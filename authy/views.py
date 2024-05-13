from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login


from post.models import Post, Follow, Stream
from django.contrib.auth.models import User
from authy.models import Profile
from .forms import *
from django.urls import resolve
from comment.models import Comment
from django.contrib.auth.views import PasswordChangeView
from django_otp.plugins.otp_email.models import EmailDevice

def UserProfile(request, username):
    Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()
    
    # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # count_comment = Comment.objects.filter(post=posts).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'profile':profile,
        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':followers_count,
        'posts_paginator':posts_paginator,
        'follow_status':follow_status,
        # 'count_comment':count_comment,
    }
    return render(request, 'profile.html', context)

def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()
            return redirect('profile', profile.user.username)
    else:
        form = EditProfileForm(instance=request.user.profile)

    context = {
        'form':form,
    }
    return render(request, 'editprofile.html', context)

def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=request.user, date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))


# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             # Profile.get_or_create(user=request.user)
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Hurray your account was created!!')

#             # Automatically Log In The User
#             new_user = authenticate(username=form.cleaned_data['username'],
#                                     password=form.cleaned_data['password1'],)
#             login(request, new_user)
#             # return redirect('editprofile')
#             return redirect('index')
            


#     elif request.user.is_authenticated:
#         return redirect('index')
#     else:
#         form = UserRegisterForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'sign-up.html', context)


def enter_otp(request, email):
    email_devices = EmailDevice.objects.filter(name=email)

    if len(email_devices) == 0:
        # No EmailDevice found with the given email
        messages.error(request, 'Invalid email. Please register again.')
        return redirect('sign-up')

    if len(email_devices) > 1:
        email_device = email_devices[0]
    else:
        email_device = email_devices.first()

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debug message
            otp = form.cleaned_data['otp_code']
            if email_device.verify_token(otp):
                new_user = User.objects.get(email=email_device.name)
                username = new_user.username
                new_user.backend = 'django.contrib.auth.backends.ModelBackend'  # Needed for login
                login(request, new_user)
                print('worked')  # Debug message
                messages.success(request, f'Hurray! Your account was created for {username}')
                return redirect('index')
            else:
                messages.error(request, 'Invalid OTP, please try again.')
        else:
            print("Form is not valid:", form.errors)  # Debug message
    else:
        form = OTPForm()

    return render(request, 'enter_otp.html', {'form': form, 'email': email_device.name})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            # Create an EmailDevice for OTP verification
            # Associate it with the newly created user
            email_device = EmailDevice.objects.create(
                user=new_user,
                name=form.cleaned_data['email']
            )
            email_device.generate_challenge()
            email_device.save()

            # Redirect to enter_otp view with email as parameter
            return redirect('enter_otp', email=email_device.name)
    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'sign-up.html',{'form':form})

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


@login_required
def password_success(request):
    return render(request, 'password_success.html', {})


@login_required
def username_reset(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        user = request.user
        user.username = new_username
        try:
            user.save()
            messages.success(request, "Username has been successfully updated.")
            return redirect('password')  # Redirect to the profile page after username reset
        except Exception as e:
            messages.error(request, "Username already exists")
            return render(request, 'username_reset.html')

    return render(request, 'username_reset.html')
                  



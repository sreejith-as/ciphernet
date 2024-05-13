from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import resolve, reverse
from django.contrib import auth, messages
from authy.models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import logout
from post.models import Follow, Report
from comment.models import Comment
from comment.forms import NewCommentForm
from django.contrib.auth.forms import AuthenticationForm


def admin_signin(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Redirect to the admin dashboard if the admin is already authenticated
        return redirect('admin_home.html')  # Update with the admin dashboard URL or view name

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()

            # Check if the authenticated user is an admin
            if user.is_staff:
                auth.login(request, user)
                # messages.success(request, 'Admin login successful.')
                return redirect('admin_home')  # Update with the admin dashboard URL or view name
            else:
                messages.error(request, 'Invalid credentials. You are not an admin.')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'admin_signin.html', {'form': form})


@login_required(login_url='admin/')
def admin_logout(request):
    logout(request)
    return redirect('admin_home')


@login_required(login_url='admin/')
def admin_home(request):
    users = User.objects.all()
    return render(request, 'admin_home.html', {'users': users})


@login_required(login_url='admin/')
def admin_search(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = User.objects.filter(Q(username__icontains=query))
        # Paginator
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)
        context = {
            'users': users_paginator,
        }
    return render(request, 'admin_search.html', context)


@login_required(login_url='admin/')
def admin_userprofile(request, username):
    Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

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
        'profile': profile,
        'posts_count': posts_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'posts_paginator': posts_paginator,
        'follow_status': follow_status,
        # 'count_comment':count_comment,
    }
    return render(request, 'admin_userprofile.html', context)


@login_required(login_url='admin/')
def admin_postdetails(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-details', args=[post.id]))
    else:
        form = NewCommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }

    return render(request, 'admin_postdetails.html', context)


@login_required(login_url='admin/')
def report_details(request):
    reports = Report.objects.all()
    return render(request, 'report_details.html', {'reports': reports})


@login_required(login_url='admin/')
def report_send(request, username):
    user = get_object_or_404(User, username=username)

    reports = Report.objects.all()
    for report in reports:

        if user == report.post.user:
            report.send = True
            report.save()

    return redirect('report_details')




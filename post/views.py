from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from post.models import Post, Tag, Follow, Stream, Likes, Report
from django.contrib.auth.models import User
from post.forms import NewPostform
from authy.models import Profile
from django.urls import resolve
from comment.models import Comment
from comment.forms import NewCommentForm
from django.core.paginator import Paginator

from django.db.models import Q


# from post.models import Post, Follow, Stream


@login_required
def index(request):
    user = request.user
    user = request.user
    all_users = User.objects.all()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    profile = Profile.objects.all()

    posts = Stream.objects.filter(user=user)
    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

    context = {
        'post_items': post_items,
        'follow_status': follow_status,
        'profile': profile,
        'all_users': all_users,
        # 'users_paginator': users_paginator,
    }
    return render(request, 'index.html', context)


@login_required
def NewPost(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    tags_obj = []

    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('profile', request.user.username)
    else:
        form = NewPostform()
    context = {
        'form': form
    }
    return render(request, 'newpost.html', context)


@login_required
def uploadtext(request):
    if request.method == "POST":
        user = request.user

        text = request.POST['upload_text']
        new_post = Post.objects.create(user=user, text=text)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')



@login_required
def PostDetail(request, post_id):
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
        'comments': comments,
        'main_user': user
    }

    return render(request, 'postdetail.html', context)


@login_required
def Tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    context = {
        'posts': posts,
        'tag': tag

    }
    return render(request, 'tag.html', context)


# Like function
@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))


@login_required
def favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)


    if request.method == 'POST':
        if post.picture:
            caption = request.POST['caption']
            tags_input = request.POST['tags']

            # Update the post fields
            post.caption = caption

            # Split tags input into individual tags
            tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
            # Update or create PostTag objects for each tag
            post.tags.clear()  # Clear existing tags
            for tag_name in tags_list:
                post_tag, _ = Tag.objects.get_or_create(title=tag_name)
                post.tags.add(post_tag)
        else:
            text = request.POST['text']
            post.text = text
        post.save()
        return redirect('post-details', post_id)  # Redirect to profile page after saving

    return render(request, 'edit_post.html', {'post': post})


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('profile', username=post.user)


@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user_object = User.objects.get(username=post.user)
    print(post)
    print(user_object)

    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            # Create a new Report object and save it
            report = Report.objects.create(
                reported_by=request.user,
                post=post,
                reason=reason
            )
            report.save()
            messages.success(request, 'Post reported successfully.')
            return redirect('post-details', post_id=post_id)
        else:
            return HttpResponseBadRequest("Please provide a reason for reporting.")

    return render(request, 'report.html', {'post': post})


@login_required
def report_view(request):
    reports = Report.objects.all()
    report_list = []

    for report in reports:
        if request.user == report.post.user:
            report_list.append(report)
        else:
            continue

    return render(request, 'notifications/report_details_user.html', {'report_list': report_list})


@login_required
def report_seen(request, username):
    user = get_object_or_404(User, username=username)

    reports = Report.objects.all()
    for report in reports:

        if user == report.post.user:
            report.seen = True
            report.save()

    return redirect('report_view')

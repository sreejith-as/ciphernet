from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from directs.models import Message
from django.contrib.auth.models import User
from authy.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator

from post.models import Post


@login_required
def inbox(request):
    user = request.user
    messages = Message.get_message(user=request.user)
    active_direct = None
    directs = None
    profile = get_object_or_404(Profile, user=user)

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=request.user, reciepient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'profile': profile,
    }
    return render(request, 'directs/direct.html', context)


@login_required
def Directs(request, username):
    user = request.user
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, reciepient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    return render(request, 'directs/direct.html', context)


def SendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        Message.sender_message(from_user, to_user, body)
        return redirect('message')


def UserSearch(request):
    context = {}
    query = request.GET.get('q')

    username_profile = []
    username_profile_list = []
    posts_by_tag = []

    if query[0] == '#':
        new_username = query[1:]
        username_object = User.objects.filter(username__icontains=new_username)

        for users in username_object:
            username_profile.append(users.id)
        posts_by_tag = []
        if new_username:
            posts_by_tag = Post.objects.filter(tags__title__icontains=new_username)
        context = {
            'username_profile_list': username_profile_list,
            'posts_by_tag': posts_by_tag,
        }
        return render(request, 'directs/tag_search.html', context)
    else:
        if query:
            users = User.objects.filter(Q(username__icontains=query))

            # Paginator
            paginator = Paginator(users, 8)
            page_number = request.GET.get('page')
            users_paginator = paginator.get_page(page_number)

            context = {
                'users': users_paginator,
                'username_profile_list': username_profile_list,

            }
        return render(request, 'directs/search.html', context)

    return render(request, 'directs/search.html', context)


def tag_search(request):
    return render(request, 'directs/search.html')


def NewConversation(request, username):
    from_user = request.user
    body = ''
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('search-users')
    if from_user != to_user:
        Message.sender_message(from_user, to_user, body)
    return redirect('message')

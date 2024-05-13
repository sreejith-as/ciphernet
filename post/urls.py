from django.urls import path
from post.views import *

urlpatterns = [
    path('', index, name='index'),
    path('newpost', NewPost, name='newpost'),

    path('uploadtext', uploadtext, name='uploadtext'),

    path('<uuid:post_id>', PostDetail, name='post-details'),
    path('tag/<slug:tag_slug>', Tags, name='tags'),
    path('<uuid:post_id>/like', like, name='like'),
    path('<uuid:post_id>/favourite', favourite, name='favourite'),


    path('post_delete/<uuid:post_id>', post_delete, name='post_delete'),
    path('post_edit/<uuid:post_id>', post_edit, name='post_edit'),


    path('report/<uuid:post_id>/', report_post, name='report_post'),
    path('report_view/', report_view, name='report_view'),
    path('report_seen/<str:username>/', report_seen, name='report_seen'),


]

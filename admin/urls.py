from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin_signin, name="admin"),
    path('admin_logout', admin_logout, name="admin_logout"),
    path('admin_home', admin_home, name="admin_home"),
    path('admin_search', admin_search, name="admin_search"),
    path('admin_userprofile/<username>', admin_userprofile, name="admin_userprofile"),
    path('admin_postdetails/<uuid:post_id>', admin_postdetails, name="admin_postdetails"),

    path('report_details', report_details, name='report_details'),
    path('report_send/<str:username>/', report_send, name='report_send'),

]

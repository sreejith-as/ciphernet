from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from authy.views import *

urlpatterns = [
    # Profile Section
    path('profile/edit', EditProfile, name="editprofile"),

    # User Authentication
    path('sign-up/', views.register, name="sign-up"),
    path('sign-in/', auth_views.LoginView.as_view(template_name="sign-in.html", redirect_authenticated_user=True), name='sign-in'),
    path('sign-out/', auth_views.LogoutView.as_view(template_name="sign-out.html"), name='sign-out'), 


    path('enter-otp/<str:email>/', views.enter_otp, name='enter_otp'),

    path('password/', PasswordsChangeView.as_view(template_name='user_password_reset.html'), name='password'),
    path('password_success/', views.password_success, name="password_success"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),


    path('username_reset/', username_reset, name="username_reset"),
]

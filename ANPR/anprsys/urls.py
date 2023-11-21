from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        '',
        views.home,
        name='home'),
    path(
        'logout/',
        views.logout_user,
        name='logout'),
    path(
        'accounts/login/',
        views.login_user,
        name='login'),
    path(
        'profile/',
        views.user_profile,
        name='user_profile'),
    path(
        'email_check',
        views.email_check,
        name='email_check'),
    path(
        'verify_email',
        views.verify_email,
        name='verify_email'),
    path(
        'temp_password',
        views.temp_password,
        name='temp_password'),
    path(
        'resend_otp/',
        views.resend_otp,
        name='resend_otp'),
    path(
        'resend_temp_password/',
        views.resend_temp_password,
        name='resend_temp_password'),
    path(
        'validate_otp/',
        views.otp_validation,
        name='otp_validation'),
    path(
        'validate_temp/',
        views.temp_validation,
        name='temp_validation'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    path('keep-alive/', views.keep_alive, name='keep_alive'),
]

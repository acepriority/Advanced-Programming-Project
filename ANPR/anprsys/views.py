from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from anprsys.models import User
from anprsys.decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from components.otp_generator import OTPGenerator
from components.temp_password_generator import TempPasswordGenerator
from datetime import datetime


@unauthenticated_user
def login_user(request):
    if request.method == "POST":
        police_id = request.POST.get('police_id')
        password = request.POST.get('password')

        user = authenticate(request, police_id=police_id, password=password)

        if user is not None:
            login(request, user)

            if police_id == password:
                otp_generator = OTPGenerator()
                otp_generator.send_otp_email(request, user.email)
                messages.success(
                    request, 'An otp has been sent to your email'
                    )
                return render(request, "otppage.html")
            else:
                messages.success(request, 'You have Been logged In!')
                return render(request, 'user_profile.html', {})
    return render(request, 'login_user.html', {})


@login_required(login_url='login_user')
def user_profile(request):
    return render(request, 'user_profile.html', {})


@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('login_user')


@login_required(login_url='login_user')
def home(request):
    return render(request, 'user_profile.html', {})


@login_required(login_url='login_user')
def resend_otp(request):
    user = request.user
    otp_generator = OTPGenerator()
    otp_generator.send_otp_email(request, user.email)
    messages.success(
        request, 'An otp has been sent to your email'
        )
    return render(request, 'otppage.html', {})


@login_required(login_url='login_user')
def otp_validation(request):
    sent_otp = request.session.get('sent_otp')
    entered_otp = request.POST.get('otp')
    expiration_time = request.session.get('expiration_time')
    expiration_date = datetime.strptime(expiration_time, "%Y-%m-%d %H:%M:%S")

    current_time = datetime.now()

    if current_time > expiration_date:
        messages.success(request, 'expired otp')
        return render(request, 'otppage.html', {})
    else:
        if sent_otp == entered_otp:
            return render(request, 'user_profile.html', {})
        else:
            messages.success(
                request, 'Invalid otp'
            )
            return render(request, 'otppage.html', {})


def email_check(request):
    return render(request, 'email.html', {})


def verify_email(request):
    if request.method == "POST":
        entered_email = request.POST.get('entered_email')

        try:
            user = User.objects.get(email=entered_email)
        except User.DoesNotExist:
            messages.error(
                request, f'User with email {entered_email} not found.')
            return render(
                request, 'your_error_template.html',
                {'error_message': f'User with email \
                    {entered_email} not found.'}
            )

        temp_password_generator = TempPasswordGenerator()
        temp_password_generator.send_temp_email(request, user.email)

        return render(request, 'temp_passwordpage.html', {'user': user})
    return render(request, 'email.html', {})


def temp_password(request):
    return render(request, 'temp_passwordpage.html', {})


def resend_temp_password(request):
    user = request.user
    temp_password_generator = TempPasswordGenerator()
    temp_password_generator.send_temp_email(request, user.email)
    messages.success(
        request, 'A temporary password has been sent to your email'
        )
    return render(request, 'temp_passwordpage.html', {})


def temp_validation(request):
    sent_temp = request.session.get('sent_temp')
    entered_temp = request.POST.get('temp_password')
    expiration_time = request.session.get('temp_expiration_time')
    expiration_date = datetime.strptime(expiration_time, "%Y-%m-%d %H:%M:%S")

    current_time = datetime.now()

    if current_time > expiration_date:
        messages.success(request, 'expired temporary password')
        return render(request, 'temp_passwordpage.html', {})
    else:
        if sent_temp == entered_temp:
            return redirect('password_reset')
        else:
            messages.success(
                request, 'Invalid temporary password'
            )
            return render(request, 'temp_passwordpage.html', {})

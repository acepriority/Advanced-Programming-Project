from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from anprsys.models import User
from anprsys.decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from components.otp_generator import OTPGenerator
from components.temp_password_generator import TempPasswordGenerator
from datetime import datetime
from django.core.cache import cache
from django.utils import timezone


@unauthenticated_user
def login_user(request):
    # Maximum number of allowed consecutive login attempts
    MAX_LOGIN_ATTEMPTS = 3
    LOCKOUT_DURATION = 300  # Lockout duration in seconds (5 minutes)
    if request.method == "POST":
        police_id = request.POST.get('police_id')
        password = request.POST.get('password')

        # Check if the user is currently locked out
        lockout_key = f'lockout_{police_id}'
        lockout_time = cache.get(lockout_key, 0)

        if lockout_time > timezone.now().timestamp():
            # User is still locked out
            remaining_lockout_time = int(
                lockout_time - timezone.now().timestamp()
                )
            messages.error(
                request,
                f'Account locked.Try again after {int(remaining_lockout_time//60)}minutes {int(remaining_lockout_time%60)} seconds.'
                )
            return render(request, 'login_user.html')

        else:
            user = authenticate(
                request,
                police_id=police_id,
                password=password
                )
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
                    cache.delete(lockout_key)
                    return redirect('home')
            else:
                # Failed login attempt
                login_attempts_key = f'login_attempts_{police_id}'
                login_attempts = cache.get(login_attempts_key, 0) + 1
                cache.set(
                    login_attempts_key,
                    login_attempts,
                    timeout=LOCKOUT_DURATION
                    )

                if login_attempts >= MAX_LOGIN_ATTEMPTS:
                    # Lockout the user for LOCKOUT_DURATION seconds
                    cache.set(
                        lockout_key,
                        timezone.now().timestamp() + LOCKOUT_DURATION,
                        timeout=LOCKOUT_DURATION
                        )
                    messages.error(
                        request,
                        f'Account locked. Try again after {int(LOCKOUT_DURATION // 60)}minutes {int(LOCKOUT_DURATION % 60)} seconds.'
                        )
                    return render(request, 'login_user.html', {})
                else:
                    # Incorrect credentials, but below the limit
                    messages.error(
                        request, 'Invalid credentials. Please try again.'
                        )
                    return render(request, 'login_user.html')
    return render(request, 'login_user.html')


@login_required(login_url='accounts/login')
def user_profile(request):
    return render(request, 'user_profile.html', {})


@login_required(login_url='accounts/login')
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('login')


@login_required(login_url='accounts/login')
def home(request):
    return render(request, 'user_profile.html', {})


@login_required(login_url='accounts/login')
def resend_otp(request):
    user = request.user
    otp_generator = OTPGenerator()
    otp_generator.send_otp_email(request, user.email)
    messages.success(
        request, 'An otp has been sent to your email'
        )
    return render(request, 'otppage.html', {})


@login_required(login_url='accounts/login')
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


@login_required(login_url='accounts/login')
def keep_alive(request):
    return JsonResponse({'status': 'ok'})

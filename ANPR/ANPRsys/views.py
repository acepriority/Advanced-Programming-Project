from django.shortcuts import render
from components.otp_generator import generate_otp
from components.temp_password_generator import temporary_password
from django.http import HttpResponse


"""def home(request):
    return render(request, 'otpemail.html')"""


def home(request):
    temporary_password()
    return HttpResponse('<h2>otp sent</h2>')

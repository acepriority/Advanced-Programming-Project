from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from components.otp_generator import OTPGenerator


def home(request):
    if request.method == "POST":
        officer_id = request.POST.get('officer_id')
        password = request.POST.get('password')

        # Check if the credentials exist in the database
        user = authenticate(request, officer_id=officer_id, password=password)

        if user is not None:
            login(request, user)
            # If the user exists in the database
            if officer_id == password:
                # If officer_id is the same as the password
                # Replace with your actual opt generation logic
                otp_generator = OTPGenerator()
                otp_generator.send_otp_email(user.email)
                messages.success(request, 'An OPT has been sent to your email')
                return render(request, "opt_confirmation.html")

            else:
                # If officer_id is not the same as the password,
                # redirect to the home page
                messages.success(request, 'You have Been logged In!')
                return redirect("home")  # Redirect to the home page

    # Render the login page for GET requests or if the login fails
    return render(request, 'home.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.....")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,
                             'You have successfully Registered, Welcome!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {
            'form': form
        })
    return render(request, 'register.html', {
            'form': form
        })

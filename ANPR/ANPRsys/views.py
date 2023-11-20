from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.http import HttpResponse
# Create your views here.

def home(request):
    if request.method == "POST":
        username = request.POST['username'] 
        password = request.POST['password']
        
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have Been logged In!')
            return redirect("home")
        else:
            messages.success(request, "There was an error logging In, Please try again...")
    else:
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
            messages.success(request, 'You have successfully Registered, Welcome!') 
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {
            'form': form
        })
    return render(request, 'register.html', {
            'form': form
        })
    
    
def process_image(request):
    if request.method == 'POST':
        # Handle image processing logic here
        # Retrieve the uploaded image using request.FILES['image']
        # Process the image using your ANPR algorithm
        # Set the result in the context to be displayed in the template
        result = "ANPR result goes here"
        return render(request, 'home.html', {'result': result})
    else:
        # Handle GET request for the process_image view if needed
        return HttpResponse("Method Not Allowed", status=405)
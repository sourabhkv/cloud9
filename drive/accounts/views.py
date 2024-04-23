# accounts/views.py  
from django.shortcuts import render, redirect  
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate, login, logout  
from django.contrib import messages  # Import messages  
import os
from django.conf import settings

def signup_view(request):  
    if request.method == 'POST':  
        # Get form values  
        name = request.POST['name']  
        email = request.POST['email']  
        password1 = request.POST['password1']  
        password2 = request.POST['password2']  
  
        # Check if passwords match  
        if password1 != password2:  
            messages.error(request, "Passwords do not match.")  
            return redirect('signup')  
  
        # Check if the email is already registered  
        if User.objects.filter(username=email).exists():  
            messages.error(request, "Email is already registered.")  
            return redirect('signup')  
  
        # If validation passes, create a new user  
        user = User.objects.create_user(username=email, email=email, password=password1)  
        user.first_name = name  # Assuming you want to store the name as the first name  
        user.save()  
  
        # Create a directory for the user in the media folder  
        user_media_path = os.path.join(settings.MEDIA_ROOT, email)  
        if not os.path.exists(user_media_path):  
            os.makedirs(user_media_path)  
  
        # Automatically log the user in after signup  
        new_user = authenticate(username=email, password=password1)  
        if new_user is not None:  
            login(request, new_user)  
            return redirect('home')  # Redirect to homepage or other appropriate page  
    else:  
        # If it's a GET request, just render the signup form  
        return render(request, 'signup.html') 


# accounts/views.py  

from django.contrib import messages  # Import messages  
  
def login_view(request):  
    if request.method == 'POST':  
        email = request.POST['email']  
        password = request.POST['password']  
        user = authenticate(request, username=email, password=password)  
        if user is not None:  
            login(request, user)  
            return redirect('home')  # Redirect to a 'home' or dashboard page after login  
        else:  
            # Add an error message  
            messages.error(request, 'Invalid login credentials')  
            return redirect('login')  # Redirect back to the login page  
    return render(request, 'signin.html')  


def logout_view(request):  
    logout(request) 
    return redirect('login')
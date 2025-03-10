from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Volunteer
# Create your views here.

def volunteer_register(request):
    if request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("volunteer_register")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("volunteer_register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("volunteer_register")

        user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
        user.save()

        volunteer = Volunteer.objects.create(user=user, phone_number=phone_number)
        volunteer.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect("login")

    return render(request, "volunteers/register.html")
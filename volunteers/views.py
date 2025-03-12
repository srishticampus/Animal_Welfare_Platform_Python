from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Volunteer, RescueRequest
from django.contrib.auth.decorators import login_required
import re
# Create your views here.

def volunteer_register(request):
    if request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        errors = {}

        if password != confirm_password:
            errors['password'] = "Passwords do not match!"
        
        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists!"

        if User.objects.filter(email=email).exists():
            errors['email'] = "Email already exists!"

        if not re.fullmatch(r"\d{10}", phone_number):
            errors['phone_number'] = "Phone number must be exactly 10 digits!"

        if errors:
            return render(request, "volunteers/register.html", {"errors": errors})

        user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
        user.save()

        volunteer = Volunteer.objects.create(user=user, phone_number=phone_number)
        volunteer.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect("login")

    return render(request, "volunteers/register.html")


@login_required
def rescue_list(request):
    rescue_requests = RescueRequest.objects.all().order_by("-created_at")
    return render(request, "volunteers/rescue_list.html", {"rescue_requests": rescue_requests})
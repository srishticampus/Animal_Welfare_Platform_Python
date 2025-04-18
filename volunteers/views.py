from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Volunteer, RescueRequest, RescueResponse
from django.contrib.auth.decorators import login_required
from donation.models import Donation
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
        profile_image = request.FILES.get('profile_image')

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

        user = User.objects.create_user(username=username, email=email, password=password, first_name=name, user_type='volunteer')
        user.is_active = False
        user.save()

        volunteer = Volunteer.objects.create(user=user, phone_number=phone_number, profile_image=profile_image)
        volunteer.save()

        messages.success(request, "Registration successful! Wait for admin approval.")
        return redirect("login")

    return render(request, "volunteers/register.html")

def volunteer_profile(request):
    volunteer = request.user
    return render(request, "volunteers/volunteer_profile.html", {"volunteer": volunteer})

def edit_volunteer_profile(request):
    user = request.user
    if request.method == "POST":
        user.username = request.POST.get('username', user.username)
        user.first_name = request.POST.get('name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.volunteer.phone_number = request.POST.get('phone_number', user.volunteer.phone_number)
        user.volunteer.profile_image = request.FILES.get('profile_image', user.volunteer.profile_image)

        user.save()
        user.volunteer.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('volunteer_profile')
    return render(request, "volunteers/edit_volunteer_profile.html", {"user": user})

@login_required
def rescue_list(request):
    volunteer = get_object_or_404(Volunteer, user=request.user)
    rescue_requests = RescueRequest.objects.all().order_by("-created_at")

    for req in rescue_requests:
        req.rejected_by_me = RescueResponse.objects.filter(
            volunteer=volunteer, rescue_request=req, rejected=True
        ).exists()

    return render(request, "volunteers/rescue_list.html", {"rescue_requests": rescue_requests})

@login_required
def accept_rescue(request, request_id):
    rescue_request = get_object_or_404(RescueRequest, id=request_id)

    if rescue_request.status == "Pending":
        volunteer = Volunteer.objects.get(user=request.user)
        rescue_request.status = "Accepted"
        rescue_request.accepted_by = volunteer
        rescue_request.save()
        messages.success(request, "You have accepted the rescue request.")
    
    return redirect("rescue_list")

@login_required
def reject_rescue(request, request_id):
    rescue_request = get_object_or_404(RescueRequest, id=request_id)
    volunteer = get_object_or_404(Volunteer, user=request.user)

    if rescue_request.status == "Pending":
        RescueResponse.objects.get_or_create(
            volunteer=volunteer, rescue_request=rescue_request, defaults={"rejected": True}
        )
        messages.success(request, "You have rejected the rescue request.")
    
    return redirect("rescue_list")

@login_required
def volunteer_dashboard(request):
    if request.user.user_type != 'volunteer':
        return redirect('home')

    donations = Donation.objects.filter(volunteer=request.user, status='approved').order_by('-created_at')
    return render(request, 'volunteers/volunteer_dashboard.html', {'donations': donations})
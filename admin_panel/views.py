from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from petshops.models import PetShop
from volunteers.models import Volunteer, RescueRequest
from .models import AddPets, AdoptionRequest
from django.contrib import messages
from donation.models import Donation
from django.contrib.admin.views.decorators import staff_member_required
from .models import Hospital
from .forms import HospitalForm
from django.db.models import Q

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("home")

    petshop_users = PetShop.objects.values_list("user_id", flat=True)
    users_count = User.objects.filter(is_superuser=False).exclude(id__in=petshop_users).count()
    volunteer_count = Volunteer.objects.count()
    petshops_count = PetShop.objects.count()

    context = {
        "users_count": users_count,
        "petshops_count": petshops_count,
        "volunteer_count": volunteer_count,
    }
    return render(request, "admin_panel/dashboard.html", context)

from itertools import chain
@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return redirect("home")

    excluded_users = list(chain(
        Volunteer.objects.values_list("user_id", flat=True),
        PetShop.objects.values_list("user_id", flat=True)
    ))
    
    search_query = request.GET.get("q", "")
    users = User.objects.filter(is_superuser=False).exclude(id__in=excluded_users)

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query)
           
        )
    return render(request, "admin_panel/manage_users.html", {"users": users,  "search_query": search_query})

def manage_volunteers(request):
    if not request.user.is_superuser:
        return redirect("home")

    volunteers = Volunteer.objects.all()
    return render(request, "admin_panel/manage_volunteers.html", {"volunteers": volunteers})

@login_required
def manage_petshops(request):
    if not request.user.is_superuser:
        return redirect("home")

    petshops = PetShop.objects.filter(user__is_active=True)
    return render(request, "admin_panel/manage_petshops.html", {"petshops": petshops})

@login_required
def petshop_requests(request):
    if not request.user.is_superuser:
        return redirect("home")
    
    petshops = PetShop.objects.filter(user__is_active=True)
    petshop_requests  = PetShop.objects.filter(user__is_active=False)
    return render(request, 'admin_panel/manage_petshop_requests.html', {"petshop_requests": petshop_requests, "petshops": petshops})



def admin_pet_list(request):
    pets = AddPets.objects.all()

    adopted_pets = {
        adoption.pet.id: adoption.user.username
        for adoption in AdoptionRequest.objects.filter(status="Approved")
    }
    print(adopted_pets)
    return render(request, "admin_panel/admin_pet_list.html", {
        "pets": pets,
        "adopted_pets": adopted_pets,
    })

@login_required
def admin_add_pet(request):
    if request.method == 'POST':
        image = request.FILES['image']
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        bread = request.POST['bread']
        size = request.POST['size']
        description = request.POST['description']
        health_vaccinations = request.POST['health_vaccinations']

        AddPets.objects.create(
            image=image,
            name=name,
            age=age,
            gender=gender,
            bread=bread,
            size=size,
            description=description,
            health_vaccinations=health_vaccinations,
            owner=request.user,
        )
        return redirect('admin_panel:admin_pet_list')

    return render(request, 'admin_panel/admin_add_pet.html')

def admin_pet_detail(request, pet_id):
    pet = get_object_or_404(AddPets, id=pet_id)
    return render(request, 'admin_panel/admin_pet_detail.html', {'pet': pet})

def admin_edit_pet(request, pet_id):
    pet = get_object_or_404(AddPets, id=pet_id)

    if request.method == 'POST':
        pet.name = request.POST['name']
        pet.age = request.POST['age']
        pet.gender = request.POST['gender']
        pet.bread = request.POST['bread']
        pet.size = request.POST['size']
        pet.description = request.POST['description']
        pet.health_vaccinations = request.POST['health_vaccinations']

        if 'image' in request.FILES:
            pet.image = request.FILES['image']

        pet.save()
        return redirect('admin_panel:admin_pet_list')

    return render(request, 'admin_panel/admin_edit_pet.html', {'pet': pet})

def admin_delete_pet(request, pet_id):
    pet = get_object_or_404(AddPets, id=pet_id)

    if request.method == 'POST':
        pet.delete()
        return redirect('admin_panel:admin_pet_list')

    return render(request, 'admin_panel/admin_delete_pet.html', {'pet': pet})

def admin_adoption_requests(request):
    requests = AdoptionRequest.objects.select_related('pet', 'user').all()
    return render(request, 'admin_panel/admin_adoption_requests.html', {'requests': requests})

def approve_adoption(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)
    adoption_request.status = 'Approved'
    adoption_request.save()

    pet = adoption_request.pet
    pet.is_adopted = True
    pet.save()
    return redirect('admin_panel:admin_adoption_requests')

def reject_adoption(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)
    adoption_request.status = 'Rejected'
    adoption_request.save()
    return redirect('admin_panel:admin_adoption_requests')

def user_toggle(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()

    return redirect('admin_panel:manage_users')

def volunteer_toggle(request, volunteer_id):
    user = User.objects.get(id=volunteer_id)
    user.is_active = not user.is_active
    user.save()

    return redirect('admin_panel:manage_volunteers')

def toggle_petshop_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()

    if user.is_active:
        messages.success(request, f"{user.username}'s account has been activated!")
        return redirect('admin_panel:petshop_requests')
    else:
        messages.warning(request, f"{user.username}'s account has been deactivated.")

    return redirect('admin_panel:petshop_requests') 


@login_required
def approve_donation(request, donation_id):
    donation = Donation.objects.get(id=donation_id)
    donation.status = 'approved'
    donation.save()
    return redirect('admin_panel:admin_dashboard')

@login_required
def admin_dashboard_donations(request):
    if not request.user.is_staff:
        return redirect('home')

    donations = Donation.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/donations.html', {'donations': donations})

def hospital_list(request):
    states = Hospital.objects.values_list('state', flat=True).distinct()
    selected_state = request.GET.get('state')
    
    if selected_state:
        hospitals = Hospital.objects.filter(state=selected_state)
    else:
        hospitals = Hospital.objects.all()

    return render(request, 'users/hospitals.html', {
        'states': states,
        'hospitals': hospitals,
        'selected_state': selected_state
    })


def hospital_list_admin(request):
    hospitals = Hospital.objects.all()
    return render(request, 'admin_panel/hospital_list.html', {'hospitals': hospitals})

def add_hospital(request):
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:hospital_list_admin')
    else:
        form = HospitalForm()
    return render(request, 'admin_panel/add_hospital.html', {'form': form})


def edit_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:hospital_list_admin')
    else:
        form = HospitalForm(instance=hospital)
    return render(request, 'admin_panel/edit_hospital.html', {'form': form, 'hospital': hospital})


def delete_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    hospital.delete()
    return redirect('admin_panel:hospital_list_admin')

@login_required
def rescue_list(request):
    rescue_requests = RescueRequest.objects.all().order_by("-created_at")


    return render(request, "admin_panel/rescue_list.html", {"rescue_requests": rescue_requests})
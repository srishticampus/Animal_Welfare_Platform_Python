from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from petshops.models import PetShop
from volunteers.models import Volunteer
from .models import AddPets, AdoptionRequest
from django.contrib import messages

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("home")

    petshop_users = PetShop.objects.values_list("user_id", flat=True)
    users_count = User.objects.filter(is_superuser=False).exclude(id__in=petshop_users).count()
    petshops_count = PetShop.objects.count()

    context = {
        "users_count": users_count,
        "petshops_count": petshops_count,
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
    
    users = User.objects.filter(is_superuser=False).exclude(id__in=excluded_users)
    return render(request, "admin_panel/manage_users.html", {"users": users})

def manage_volunteers(request):
    if not request.user.is_superuser:
        return redirect("home")

    volunteers = Volunteer.objects.all()
    return render(request, "admin_panel/manage_volunteers.html", {"volunteers": volunteers})

@login_required
def manage_petshops(request):
    if not request.user.is_superuser:
        return redirect("home")

    petshops = PetShop.objects.all()
    return render(request, "admin_panel/manage_petshops.html", {"petshops": petshops})


def admin_pet_list(request):
    pets = AddPets.objects.all()
    return render(request, 'admin_panel/admin_pet_list.html', {'pets': pets})

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
            health_vaccinations=health_vaccinations
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
    return redirect('admin_adoption_requests')

def user_toggle(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = not user.is_active
    user.save()

    return redirect('manage_users')

def toggle_petshop_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()

    if user.is_active:
        messages.success(request, f"{user.username}'s account has been activated!")
        return redirect('admin_panel:manage_petshops')
    else:
        messages.warning(request, f"{user.username}'s account has been deactivated.")

    return redirect('admin_panel:manage_petshops') 
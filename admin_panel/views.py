from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from petshops.models import PetShop

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

@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return redirect("home")

    petshop_users = PetShop.objects.values_list("user_id", flat=True)
    users = User.objects.filter(is_superuser=False).exclude(id__in=petshop_users)
    return render(request, "admin_panel/manage_users.html", {"users": users})

@login_required
def manage_petshops(request):
    if not request.user.is_superuser:
        return redirect("home")

    petshops = PetShop.objects.all()
    return render(request, "admin_panel/manage_petshops.html", {"petshops": petshops})

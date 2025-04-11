from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Donation
from accounts.models import User

@login_required
def donation_page(request):
    volunteers = User.objects.filter(user_type='volunteer')
    return render(request, 'donation/donation_page.html', {'volunteers': volunteers})

@login_required
def make_donation(request, volunteer_id):
    if request.method == "POST":
        amount = request.POST.get('amount')
        volunteer = User.objects.get(id=volunteer_id)
        
        donation = Donation.objects.create(donor=request.user, volunteer=volunteer, amount=amount)
        return redirect('donation_page')

    return redirect('donation_page')

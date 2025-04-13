from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import ContactUs
# Create your views here.

def landing_page(request):
    return render(request, 'landing/landing_page.html')

def about_page(request):
    return render(request, 'landing/about.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        comments = request.POST['comments']

        contact_us = ContactUs(name=name, email=email, comments=comments)
        contact_us.save()

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact_page')

    return render(request, 'landing/contact.html')
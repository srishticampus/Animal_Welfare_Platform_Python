from django.shortcuts import render

# Create your views here.

def landing_page(request):
    return render(request, 'landing/landing_page.html')

def about_page(request):
    return render(request, 'landing/about.html')

def contact_page(request):
    return render(request, 'landing/contact.html')
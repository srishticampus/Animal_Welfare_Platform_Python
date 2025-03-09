from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from petshops.models import Product, Cart
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from datetime import datetime

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        aadhaar_number = request.POST['aadhaar_number']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        profile_image = request.FILES.get('profile_image')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        profile = UserProfile.objects.create(user=user, aadhaar_number=aadhaar_number, phone_number=phone_number, profile_image=profile_image)
        
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'users/register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('login')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


def home(request):
    return render(request, 'users/pet-shop.html')

def pet_shop(request):
    products = Product.objects.all()
    return render(request, 'users/pet-shop.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'users/product_detail.html', {'product': product})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    similar_products = Product.objects.exclude(id=product_id)[:3]
    return render(request, 'users/product_detail.html', {'product': product, 'similar_products': similar_products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_page')

def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    
    tax_rate = Decimal('0.10')
    tax_amount = total_price * tax_rate
    final_price = total_price + tax_amount

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "tax_amount": tax_amount,
        "final_price": final_price,
    }
    return render(request, 'users/cart.html', context)

def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart_page')

def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart")
    
    total_price = sum(item.total_price() for item in cart_items)
    tax_rate = Decimal('0.10')
    tax_amount = total_price * tax_rate
    final_price = total_price + tax_amount

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "tax_amount": tax_amount,
        "final_price": final_price,
    }
    return render(request, "users/checkout.html", context)



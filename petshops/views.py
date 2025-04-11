from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import PetShop, Product, Order, OrderItem
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re

def register_petshop(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        registration_id = request.POST['registration_id']
        phone_number = request.POST['phone_number']
        location = request.POST['location']
        available_accessories = request.POST['available_accessories']

        errors = {}

    
        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists!"

     
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Invalid email format!"

        if User.objects.filter(email=email).exists():
            errors['email'] = "Email already exists!"

       
        if PetShop.objects.filter(registration_id=registration_id).exists():
            errors['registration_id'] = "This Registration ID is already taken!"

        if not re.fullmatch(r"\d{10}", phone_number):
            errors['phone_number'] = "Phone number must be exactly 10 digits!"

     
        if password != confirm_password:
            errors['password'] = "Passwords do not match!"

        if errors:
            return render(request, 'petshops/register.html', {'errors': errors})

        user = User.objects.create_user(username=username, email=email, password=password, user_type='petshop')
        user.is_active = False
        user.save()
        PetShop.objects.create(
            user=user,
            registration_id=registration_id,
            phone_number=phone_number,
            location=location,
            available_accessories=available_accessories
        )
        messages.success(request, "Registration successful! Your account will be reviewed by an admin.")
        return redirect('login')

    return render(request, 'petshops/register.html')

def login_petshop(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('add_product')  
        return render(request, 'petshops/login.html', {'error': 'Invalid credentials'})

    return render(request, 'petshops/login.html')

@login_required
def add_product_page(request):
    petshop = PetShop.objects.get(user=request.user)
    
    if request.method == 'POST':
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_description = request.POST['product_description']
        product_image = request.FILES['product_image']

        Product.objects.create(
            petshop=petshop,
            product_name=product_name,
            product_price=product_price,
            product_description=product_description,
            product_image=product_image
        )
        messages.success(request, 'Item added')
        return redirect('add_product')
    return render(request, 'petshops/add_product.html')

def list_product(request):
    petshop = PetShop.objects.get(user=request.user)
    products = Product.objects.filter(petshop=petshop)
    return render(request, 'petshops/list_products.html', {'products': products})

def shop_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        petshop = PetShop.objects.get(user=request.user)
    except PetShop.DoesNotExist:
        return redirect('some_error_page')

    order_items = OrderItem.objects.filter(product__petshop=petshop)


    orders = Order.objects.filter(order_items__in=order_items).distinct()

    return render(request, 'petshops/shope_orders.html', {
        'orders': orders,
        'petshop': petshop
    })
    

def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.success(request, 'Item deleted')
    return redirect('list_products')

def logout_petshop(request):
    logout(request)
    return redirect('login_petshop')
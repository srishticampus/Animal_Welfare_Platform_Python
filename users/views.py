from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from admin_panel.models import AddPets
from petshops.models import Product, Cart, Order, OrderItem, Payment, ShippingAddress
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from datetime import datetime
from petshops.models import PetShop
from volunteers.models import Volunteer, RescueRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from admin_panel.models import AddPets, AdoptionRequest, AdoptionApplication
import re 
from django.http import JsonResponse
import json

def register(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        aadhaar_number = request.POST.get('aadhaar_number', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        profile_image = request.FILES.get('profile_image')

        errors = {}

        if not profile_image:
            errors['profile_image'] = "Profile image is required!"

        if username.isdigit():
            errors['username'] = "Username cannot be entirely numeric!"

    
        if not re.fullmatch(r'^\d{10}$', phone_number):
            errors['phone_number'] = "Phone number must be exactly 10 digits!"

    
        if not aadhaar_number.isdigit():
            errors['aadhaar_number'] = "Aadhaar number must contain only numbers!"

        
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long!"

    
        if password != confirm_password:
            errors['confirm_password'] = "Passwords do not match!"

       
        if User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists!"

   
        if User.objects.filter(email=email).exists():
            errors['email'] = "Email already exists!"

        if errors:
            return render(request, 'users/register.html', {'errors': errors})

   
        user = User.objects.create_user(username=username, email=email, password=password, user_type='normal')
        UserProfile.objects.create(user=user, aadhaar_number=aadhaar_number, phone_number=phone_number, profile_image=profile_image)

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'users/register.html', {'errors': {}})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            if not user.is_active:
                messages.error(request, "Your account is pending approval by the admin.")
                return redirect('login')
            login(request, user)
            if user.is_superuser:  
                return redirect("admin_panel:admin_dashboard") 
            elif PetShop.objects.filter(user=user).exists():
                messages.success(request, "Login successful!")
                return redirect("add_product")  
            elif Volunteer.objects.filter(user=user).exists():
                messages.success(request, "Login successful!")
                return redirect("rescue_list")
            else:
                messages.success(request, "Login successful!")
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'users/login.html')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            request.session['reset_email'] = email  
            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, "Email does not exist.")
    
    return render(request, 'users/forgot-password.html')


def reset_password(request):
    if 'reset_email' not in request.session:
        return redirect('forgot_password')  
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            user = User.objects.get(email=request.session['reset_email'])
            user.set_password(password)
            user.save()
            del request.session['reset_email'] 
            messages.success(request, "Password reset successfully. You can now log in.")
            return redirect('login')

    return render(request, 'users/reset_password.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@never_cache
@login_required
def home(request):
    products = Product.objects.order_by('-id')[:3]
    pets = AddPets.objects.order_by('-id')[:3]
    
    return render(request, 'users/home.html', {'products': products ,'pets': pets})

@never_cache
@login_required
def pet_shop(request):
    products = Product.objects.all()
    return render(request, 'users/pet-shop.html', {'products': products})

@never_cache
@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'users/product_detail.html', {'product': product})

@never_cache
@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    similar_products = Product.objects.exclude(id=product_id)[:3]
    return render(request, 'users/product_detail.html', {'product': product, 'similar_products': similar_products})

@never_cache
@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)
        
        product = get_object_or_404(Product, id=product_id)
        
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if created:
            cart_item.quantity = quantity  
        else:
            cart_item.quantity += 1  

        cart_item.save()
    
        messages.success(request, 'Item added')
        return JsonResponse({"message": "Product added to cart!"}, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@never_cache
@login_required
def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty. Add some items before checking out.")
    
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

@never_cache
@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart_page')

# def checkout(request):
#     cart_items = Cart.objects.filter(user=request.user)
    
#     if not cart_items.exists():
#         messages.error(request, "Your cart is empty.")
#         return redirect("cart")
    
#     total_price = sum(item.total_price() for item in cart_items)
#     tax_rate = Decimal('0.10')
#     tax_amount = total_price * tax_rate
#     final_price = total_price + tax_amount

#     context = {
#         "cart_items": cart_items,
#         "total_price": total_price,
#         "tax_amount": tax_amount,
#         "final_price": final_price,
#     }
#     return render(request, "users/checkout.html", context)

@never_cache
@login_required
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

    if request.method == "POST":
        address = request.POST["address"]
        pin_code = request.POST["pin_code"]
        phone = request.POST["phone"]
        
        shipping_address = ShippingAddress.objects.create(
            user=request.user,
            name=request.user.username,
            email=request.user.email,
            phone=phone,
            address=address,
            pin_code=pin_code
        )
        
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        
        payment = Payment.objects.create(
            user=request.user,
            card_number=request.POST["card_number"],
            card_name=request.POST["card_name"],
            expiry_date=request.POST["expiry_date"],
            cvv=request.POST["cvv"]
        )
        
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            payment=payment,
            total_price=total_price
        )
        
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.total_price())
        
        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect("order_success", order_id=order.id)
    
    return render(request, "users/checkout.html", context)

@never_cache
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    cart_items = Cart.objects.filter(user=request.user)

    total_price = sum(item.total_price() for item in cart_items)
    tax_rate = Decimal('0.10')
    tax_amount = order.total_price * tax_rate
    final_price = order.total_price + tax_amount

    context = {
        "items": items,
        "total_price": total_price,
        "tax_amount": tax_amount,
        "final_price": final_price,
        'order': order,
    }

    return render(request, "users/order_success.html", context)

def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/orders.html', {'orders': orders})

@never_cache
@login_required
def pet_adoption_list(request):
    pets = AddPets.objects.all()
    return render(request, 'users/pet_adoption_list.html', {'pets': pets})

@never_cache
@login_required
def pet_adoption_detail(request, pet_id):
    pet = get_object_or_404(AddPets, id=pet_id)


    existing_request = AdoptionRequest.objects.filter(pet=pet, user=request.user).first()
    
    if request.method == 'POST' and not existing_request:
        AdoptionRequest.objects.create(pet=pet, user=request.user, status='Pending')
        messages.success(request, 'Adoption request sent successfully!')
        return redirect('pet_adoption_detail', pet_id=pet.id)


    adopted_user = AdoptionRequest.objects.filter(pet=pet, status="Approved").first()

    pet_owner = pet.owner

    return render(request, 'users/pet_adoption_detail.html', {
        'pet': pet,
        'existing_request': existing_request, 
        'adopted_user': adopted_user.user.username if adopted_user else None,
        'pet_owner': pet_owner  
    })

@never_cache
@login_required
def adoption_form(request, pet_id):
    pet = get_object_or_404(AddPets, id=pet_id)
    adoption_request, created = AdoptionRequest.objects.get_or_create(pet=pet, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        experience = request.POST.get('experience')
        reason = request.POST.get('reason')

        AdoptionApplication.objects.create(
            adoption_request=adoption_request,
            name=name,
            email=email,
            phone=phone,
            address=address,
            experience=experience,
            reason=reason
        )
        messages.success(request, 'Form Submitted Successfully!')
        return redirect('pet_adoption_list') 

    return render(request, 'users/adoption_form.html', {'pet': pet})

@never_cache
@login_required
def create_rescue_request(request):
    if request.method == "POST":
        location = request.POST["location"]
        description = request.POST["description"]
        image = request.FILES.get("image") 

        RescueRequest.objects.create(
            user=request.user,
            location=location,
            description=description,
            image=image
        )
        
        messages.success(request, "Rescue request submitted successfully!")
        return redirect("create_rescue_request")  

    return render(request, "users/rescue.html")


@login_required
def add_pet(request):
    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST["age"]
        gender = request.POST["gender"]
        breed = request.POST["breed"]
        size = request.POST["size"]
        description = request.POST["description"]
        health_vaccinations = request.POST["health_vaccinations"]
        image = request.FILES["image"]

        pet = AddPets.objects.create(
            name=name,
            age=age,
            gender=gender,
            bread=breed,
            size=size,
            description=description,
            health_vaccinations=health_vaccinations,
            image=image,
            owner=request.user, 
        )
        return redirect("pet_adoption_list")

    return render(request, "users/add_pet.html")


@login_required
def user_pets_list(request):
    """List all pets available for adoption (excluding those already adopted)"""
    pets = AddPets.objects.filter(is_adopted=False).exclude(owner=request.user) 
    return render(request, "users/user_pets_list.html", {"pets": pets})


@login_required
def apply_for_adoption(request, pet_id):
    pet = get_object_or_404(AddPets, id=pet_id)

    # Ensure users cannot apply for their own pet
    if pet.owner == request.user:
        return redirect("user_pets_list")

    AdoptionRequest.objects.create(pet=pet, adopter=request.user, owner=pet.owner)
    return redirect("user_pets_list")


@login_required
def manage_adoption_requests(request):
    """List all adoption requests for pets the user owns."""
    requests = AdoptionRequest.objects.filter(owner=request.user)
    return render(request, "usersmanage_adoption_requests.html", {"requests": requests})


@login_required
def update_adoption_status(request, request_id, status):
    """Approve or Reject an adoption request"""
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)

    # Ensure only the pet owner can update the status
    if adoption_request.owner != request.user:
        return redirect("manage_adoption_requests")

    adoption_request.status = status
    if status == "Approved":
        adoption_request.pet.is_adopted = True  # Mark pet as adopted
        adoption_request.pet.save()

    adoption_request.save()
    return redirect("manage_adoption_requests")
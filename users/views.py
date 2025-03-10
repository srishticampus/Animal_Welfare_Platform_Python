from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from petshops.models import Product, Cart, Order, OrderItem, Payment, ShippingAddress
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from datetime import datetime
from petshops.models import PetShop
from volunteers.models import Volunteer, RescueRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from admin_panel.models import AddPets, AdoptionRequest, AdoptionApplication

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

        if user:
            login(request, user)
            if user.is_superuser:  
                return redirect("admin_dashboard") 
            elif PetShop.objects.filter(user=user).exists():
                return redirect("add_product")  
            elif Volunteer.objects.filter(user=user).exists():
                return redirect("volunteer_dashboard")
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@never_cache
@login_required
def home(request):
    return render(request, 'users/pet-shop.html')

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
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_page')

@never_cache
@login_required
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

def pet_adoption_list(request):
    pets = AddPets.objects.filter(is_adopted=False)
    return render(request, 'users/pet_adoption_list.html', {'pets': pets})

def pet_adoption_detail(request, pet_id):
    pet = get_object_or_404(AddPets, id=pet_id)


    existing_request = AdoptionRequest.objects.filter(pet=pet, user=request.user).first()
    
    if request.method == 'POST':
        if not existing_request:
            AdoptionRequest.objects.create(pet=pet, user=request.user)
            return redirect('pet_adoption_list')

    return render(request, 'users/pet_adoption_detail.html', {'pet': pet, 'existing_request': existing_request})

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
        return redirect("rescue_list")  

    return render(request, "users/rescue.html")
from django.urls import path
from .views import register, login_view, logout_view, home, pet_shop, product_detail, cart_page, add_to_cart, remove_from_cart, checkout,order_success,pet_adoption_list,pet_adoption_detail,adoption_form,create_rescue_request,forgot_password,reset_password,user_orders

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('', home, name='home'),
    path('petshop/', pet_shop, name='petshop'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', cart_page, name='cart_page'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path("checkout/", checkout, name="checkout"),
    path("order-success/<int:order_id>/", order_success, name="order_success"),
    path('orders/', user_orders, name='user_orders'),
    path('adopt/', pet_adoption_list, name='pet_adoption_list'),
    path('adopt/<int:pet_id>/', pet_adoption_detail, name='pet_adoption_detail'),
    path('adoption-form/<int:pet_id>/', adoption_form, name='adoption_form'),
    path("rescue/", create_rescue_request, name="create_rescue_request"),
    path('reset-password/', reset_password, name='reset_password'),

 

]
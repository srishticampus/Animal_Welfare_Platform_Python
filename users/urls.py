from django.urls import path
from .views import register, login_view, logout_view, home, pet_shop, product_detail, cart_page, add_to_cart, remove_from_cart, checkout

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),
    path('petshop/', pet_shop, name='petshop'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', cart_page, name='cart_page'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path("checkout/", checkout, name="checkout"),
 

]
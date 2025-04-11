from django.urls import path
from .views import register_petshop, login_petshop, add_product_page, logout_petshop,list_product,shop_orders

urlpatterns = [
    path('register/', register_petshop, name='register_petshop'),
    path('login/', login_petshop, name='login_petshop'),
    path('add-product/', add_product_page, name='add_product'),
    path('list-products/', list_product, name='list_products'),
    path('logout/', logout_petshop, name='logout_petshop'),
    path("shop/orders/", shop_orders, name="shop_orders"),

]

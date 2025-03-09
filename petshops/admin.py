from django.contrib import admin
from .models import PetShop, Product, Cart, Order, OrderItem, Payment, ShippingAddress
# Register your models here.


admin.site.register(PetShop)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(ShippingAddress)


from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, Permission
# Create your models here.


class PetShop(models.Model):
    name = models.CharField(max_length=255)
    registration_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    location = models.TextField()
    available_accessories = models.TextField()
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, related_name="petshop_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="petshop_user_permissions", blank=True)

    def __str__(self):
        return self.name

    
class PetShopProduct(models.Model):
    shop = models.ForeignKey(PetShop, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"{self.name} - {self.shop.name}"
    

class Offer(models.Model):
    product = models.ForeignKey(PetShopProduct, on_delete=models.CASCADE, related_name='offers')
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"Offer on {self.product.name}"
from django.db import models
from django.contrib.auth.models import User

class PetShop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    location = models.TextField()
    available_accessories = models.TextField()

    def __str__(self):
        return self.user.username

class Product(models.Model):
    petshop = models.ForeignKey(PetShop, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product_name
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.product_price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} - {self.quantity}"
    


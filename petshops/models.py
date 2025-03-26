from django.db import models
from accounts.models import User

# ------------------- PET SHOP -------------------
class PetShop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    location = models.TextField()
    available_accessories = models.TextField()

    def __str__(self):
        return self.user.username


# ------------------- PRODUCTS -------------------
class Product(models.Model):
    petshop = models.ForeignKey(PetShop, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product_name


# ------------------- CART -------------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.product_price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} - {self.quantity}"


# ------------------- SHIPPING ADDRESS -------------------
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    landmark = models.CharField(max_length=255, blank=True, null=True)
    pin_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username} - {self.address}"


# ------------------- PAYMENT -------------------
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_name = models.CharField(max_length=255)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.user.username} - {self.card_number[-4:]}"


# ------------------- ORDER -------------------
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


# ------------------- ORDER ITEMS -------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

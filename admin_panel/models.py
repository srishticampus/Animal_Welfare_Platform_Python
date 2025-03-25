from django.db import models
from accounts.models import User
# Create your models here.

class AddPets(models.Model):
    image = models.ImageField(upload_to='pet_images/')
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    bread = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    health_vaccinations = models.CharField(max_length=100)
    is_adopted = models.BooleanField(default=False) 

    def __str__(self):
        return self.name
    

class AdoptionRequest(models.Model):
    pet = models.ForeignKey(AddPets, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending'
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        return f"{self.user.username} - {self.pet.name} ({self.status})"


class AdoptionApplication(models.Model):
    adoption_request = models.ForeignKey(AdoptionRequest, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    experience = models.TextField()
    reason = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
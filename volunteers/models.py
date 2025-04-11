from django.db import models
from accounts.models import User

# Create your models here.
class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.user.username
    

class RescueRequest(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    location = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to="rescue_images/", blank=True, null=True)
    predicted_animal = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    accepted_by = models.ForeignKey(Volunteer, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Rescue Request by {self.user.username} at {self.location}"
    

class RescueResponse(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    rescue_request = models.ForeignKey(RescueRequest, on_delete=models.CASCADE)
    rejected = models.BooleanField(default=False)

    class Meta:
        unique_together = ("volunteer", "rescue_request") 

    def __str__(self):
        return f"{self.volunteer.user.username} {'Rejected' if self.rejected else 'Accepted'} Request {self.rescue_request.id}"
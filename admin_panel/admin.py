from django.contrib import admin
from .models import AddPets, AdoptionRequest, AdoptionApplication
# Register your models here.

admin.site.register(AddPets)
admin.site.register(AdoptionRequest)
admin.site.register(AdoptionApplication)
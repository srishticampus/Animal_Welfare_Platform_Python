from django.contrib import admin
from .models import UserProfile, ContactUs
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(ContactUs)
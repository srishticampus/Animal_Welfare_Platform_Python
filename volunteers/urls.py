from django.urls import path
from .views import volunteer_register

urlpatterns = [
    path('register/', volunteer_register, name='volunteer_register'),
]
from django.urls import path
from .views import volunteer_register, rescue_list

urlpatterns = [
    path('register/', volunteer_register, name='volunteer_register'),
    path("rescue-list/", rescue_list, name="rescue_list"),
]
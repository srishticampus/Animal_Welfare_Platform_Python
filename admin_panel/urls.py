from django.urls import path
from .views import admin_dashboard, manage_users, manage_petshops

urlpatterns = [
    path("", admin_dashboard, name="admin_dashboard"),
    path("users/", manage_users, name="manage_users"),
    path("petshops/", manage_petshops, name="manage_petshops"),
]

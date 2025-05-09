from django.urls import path
from .views import admin_dashboard, manage_users, manage_petshops
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path("", admin_dashboard, name="admin_dashboard"),
    path("users/", manage_users, name="manage_users"),
    path("petshops/", manage_petshops, name="manage_petshops"),
    path('petshop-requests', views.petshop_requests, name='petshop_requests'),
    path('volunteers/', views.manage_volunteers, name='manage_volunteers'),
    path('admin/pets/', views.admin_pet_list, name='admin_pet_list'),
    path('admin/pets/add/', views.admin_add_pet, name='admin_add_pet'),
    path('admin/pets/<int:pet_id>/', views.admin_pet_detail, name='admin_pet_detail'),
    path('admin/pets/<int:pet_id>/edit/', views.admin_edit_pet, name='admin_edit_pet'),
    path('admin/pets/<int:pet_id>/delete/', views.admin_delete_pet, name='admin_delete_pet'),

    path('admin/adoption-requests/', views.admin_adoption_requests, name='admin_adoption_requests'),
    path('admin/adoption-requests/<int:request_id>/approve/', views.approve_adoption, name='approve_adoption'),
    path('admin/adoption-requests/<int:request_id>/reject/', views.reject_adoption, name='reject_adoption'),
    path('user_toggle/<int:user_id>/', views.user_toggle, name='user_toggle'),
    path('volunteer_toggle/<int:volunteer_id>/', views.volunteer_toggle, name='volunteer_toggle'),
    path('toggle_petshop_status/<int:user_id>/', views.toggle_petshop_status, name='toggle_petshop_status'),

    path('admin/donations/', views.admin_dashboard_donations, name='admin_dashboard_donations'),
    path('admin/approve/<int:donation_id>/', views.approve_donation, name='approve_donation'),

    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('hospital_list/', views.hospital_list_admin, name='hospital_list_admin'),
    path('hospitals/add/', views.add_hospital, name='add_hospital'),
    path('hospitals/edit/<int:hospital_id>/', views.edit_hospital, name='edit_hospital'),
    path('hospitals/delete/<int:hospital_id>/', views.delete_hospital, name='delete_hospital'),

    path("rescue-list/", views.rescue_list, name="rescue_list"),

]

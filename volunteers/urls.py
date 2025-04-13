from django.urls import path
from .views import volunteer_register, rescue_list, accept_rescue, reject_rescue,volunteer_dashboard, volunteer_profile, edit_volunteer_profile

urlpatterns = [
    path('register/', volunteer_register, name='volunteer_register'),
    path("rescue-list/", rescue_list, name="rescue_list"),
    path('accept_rescue/<int:request_id>', accept_rescue, name='accept_rescue'),
    path('reject_rescue/<int:request_id>', reject_rescue, name='reject_rescue'),
    path('volunteer/donations/', volunteer_dashboard, name='volunteer_dashboard'),
    path('volunteer/profile/', volunteer_profile, name='volunteer_profile'),
    path('volunteer/edit-profile/', edit_volunteer_profile, name='edit_volunteer_profile'),


]
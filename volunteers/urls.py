from django.urls import path
from .views import volunteer_register, rescue_list, accept_rescue, reject_rescue

urlpatterns = [
    path('register/', volunteer_register, name='volunteer_register'),
    path("rescue-list/", rescue_list, name="rescue_list"),
    path('accept_rescue/<int:request_id>', accept_rescue, name='accept_rescue'),
    path('reject_rescue/<int:request_id>', reject_rescue, name='reject_rescue'),

]
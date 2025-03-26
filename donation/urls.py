from django.urls import path
from . import views

urlpatterns = [
    path('donation/', views.donation_page, name='donation_page'),
    path('donate/<int:volunteer_id>/', views.make_donation, name='make_donation'),


]

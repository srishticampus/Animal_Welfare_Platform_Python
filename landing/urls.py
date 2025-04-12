from django.urls import path
from .views import landing_page, about_page, contact_us

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("about/", about_page, name="about_page"),
    path("contact/", contact_us, name="contact_page"),
    
]
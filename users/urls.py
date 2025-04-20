from django.urls import path
from .views import register, login_view, logout_view, home, pet_shop, product_detail, cart_page, add_to_cart, remove_from_cart, checkout,order_success,pet_adoption_list,pet_adoption_detail,adoption_form,create_rescue_request,forgot_password,reset_password,user_orders, add_pet, user_pets_list, apply_for_adoption, manage_adoption_requests, update_adoption_status, predict_image, user_profile, edit_user_profile, user_rescue_list, my_donations

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('', home, name='home'),
    path('petshop/', pet_shop, name='petshop'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path("cart/", cart_page, name="cart"),
    path('cart/', cart_page, name='cart_page'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    path("checkout/", checkout, name="checkout"),
    path("order-success/<int:order_id>/", order_success, name="order_success"),
    path('orders/', user_orders, name='user_orders'),
    path('adopt/', pet_adoption_list, name='pet_adoption_list'),
    path('adopt/<int:pet_id>/', pet_adoption_detail, name='pet_adoption_detail'),
    path('adoption-form/<int:pet_id>/', adoption_form, name='adoption_form'),
    path("rescue/", create_rescue_request, name="create_rescue_request"),
    path('reset-password/', reset_password, name='reset_password'),
    path('profile/', user_profile, name='user_profile'),
    path('edit-profile/', edit_user_profile, name='edit_user_profile'),

    path("user_rescue-list/", user_rescue_list, name="user_rescue_list"),
    path("my-donations/", my_donations, name="my_donations"),


    path("add-pet/", add_pet, name="add_pet"),
    path("user-pets/", user_pets_list, name="user_pets_list"),
    path("apply-for-adoption/<int:pet_id>/", apply_for_adoption, name="apply_for_adoption"),
    path("manage-requests/", manage_adoption_requests, name="manage_adoption_requests"),
    path("update-adoption-status/<int:request_id>/<str:status>/", update_adoption_status, name="update_adoption_status"),
    path("predict/", predict_image, name="predict_image"),

 

]
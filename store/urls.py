from django.urls import path

from . import views
from .views import resetpassword

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("search", views.search, name="search"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("cart",views.cart,name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("profile",views.view_profile,name="view_profile"),
    path("profile/edit",views.edit_profile,name="edit_profile"),
    path("profile/resetpassword",views.resetpassword,name="resetpassword"),
    path("update_item", views.update_item, name="update_item"),
    path("process_order", views.processOrder, name="process_order"),
    path("view_product/<int:id>", views.view_product, name="view_product"),
    path("categories", views.categories, name="categories"),
    path("aboutus", views.aboutUs, name="aboutUs"),
    path("contactus", views.contactUs, name="contactUs"),



]

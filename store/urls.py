from django.urls import path
from . import views

urlpatterns = [
    #Login
    path("login/", views.loginPage, name="login"),

    #Register
    path("register/", views.registerPage, name="register"),

    #Logout
    path("logout/", views.logoutPage, name="logout"),

    #Order
    path("order/", views.orderPage, name="order"),
]

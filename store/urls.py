from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout/", views.logoutPage, name="logout"),

    # Products
    path("products/", views.all_products, name="all_products"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),

    # Basket (New)
    path("basket/", views.view_basket, name="view_basket"),
    path("basket/add/<int:product_id>/", views.add_to_basket, name="add_to_basket"),
    path("basket/update/<int:product_id>/", views.update_basket, name="update_basket"),
    path("basket/remove/<int:product_id>/", views.remove_from_basket, name="remove_from_basket"),
    path("basket/empty/", views.empty_basket, name="empty_basket"),

    # Order
    path("order/", views.orderPage, name="order"),
]

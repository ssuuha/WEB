from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import Product, Order, OrderItem
from .forms import RegisterForm, LoginForm


# Login Page 
def loginPage(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("/store/products/")
    else:
        form = LoginForm()

    return render(request, "store/login.html", {"form": form})


#Registration Page 
def registerPage(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "store/register.html", {"form": form})


# Logout Functionality
def logoutPage(request):
    logout(request)
    return redirect("login")


#Order Page
def orderPage(request):
    if request.method != "POST":
        basket = request.session.get("basket", [])
        return render(request, "store/order.html", {
            "basket": basket
        })

    basket = request.session.get("basket", [])

    order = Order.objects.create(
        user=request.user,
        total=0
    )

    total = 0
    for item in basket:
        product = Product.objects.get(id=item["product_id"])
        qty = item["quantity"]

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty
        )

        total += product.price * qty

    order.total = total
    order.save()

    request.session["basket"] = []

    return HttpResponseRedirect(reverse("order"))

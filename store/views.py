from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Order, OrderItem
from .forms import RegisterForm, LoginForm

# --- AUTHENTICATION ---

def loginPage(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("all_products")
    else:
        form = LoginForm()
    return render(request, "store/login.html", {"form": form})

def registerPage(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please login.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "store/register.html", {"form": form})

def logoutPage(request):
    logout(request)
    return redirect("login")

# --- PRODUCTS ---

def all_products(request):
    products = Product.objects.all()
    return render(request, "store/all_products.html", {
        "products": products
    })

def product_detail(request, product_id):
     product = get_object_or_404(Product, id=product_id)
     return render(request, "store/product_detail.html", {
        "product": product
    })

# --- BASKET LOGIC (Req 6) ---

def add_to_basket(request, product_id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        basket = request.session.get("basket", [])

        # Check if product is already in basket
        found = False
        for item in basket:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                found = True
                break
        
        if not found:
            basket.append({"product_id": product_id, "quantity": quantity})

        request.session["basket"] = basket
        messages.success(request, "Item added to basket.")
        return redirect("all_products")

def view_basket(request):
    basket_session = request.session.get("basket", [])
    basket_items = []
    total_cost = 0

    # We need to fetch the actual Product objects to show names/images
    for item in basket_session:
        product = Product.objects.get(id=item["product_id"])
        total_price = product.price * item["quantity"]
        total_cost += total_price
        
        basket_items.append({
            "product": product,
            "quantity": item["quantity"],
            "total_price": total_price
        })

    return render(request, "store/basket.html", {
        "basket_items": basket_items,
        "total_cost": total_cost
    })

def update_basket(request, product_id):
    if request.method == "POST":
        new_qty = int(request.POST.get("quantity", 1))
        basket = request.session.get("basket", [])

        for item in basket:
            if item["product_id"] == product_id:
                if new_qty > 0:
                    item["quantity"] = new_qty
                else:
                    basket.remove(item)
                break
        
        request.session["basket"] = basket
        messages.info(request, "Basket updated.")
    return redirect("view_basket")

def remove_from_basket(request, product_id):
    basket = request.session.get("basket", [])
    
    # Filter out the item to remove it
    basket = [item for item in basket if item["product_id"] != product_id]
    
    request.session["basket"] = basket
    messages.warning(request, "Item removed from basket.")
    return redirect("view_basket")

def empty_basket(request):
    request.session["basket"] = []
    messages.warning(request, "Basket emptied.")
    return redirect("view_basket")

# --- ORDER LOGIC ---

@login_required
def orderPage(request):
    # Retrieve basket
    basket_session = request.session.get("basket", [])

    if request.method == "POST":
        # Create the Order
        if not basket_session:
            return redirect("view_basket")

        order = Order.objects.create(user=request.user, total=0)
        total = 0

        for item in basket_session:
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

        # Clear basket
        request.session["basket"] = []
        messages.success(request, "Order placed successfully!")
        return render(request, "store/order.html", {"order": order})

    # If GET request, show summary (simplified for this assignment)
    return redirect("view_basket")

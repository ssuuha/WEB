from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product, Order, OrderItem
# Create your views here.

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

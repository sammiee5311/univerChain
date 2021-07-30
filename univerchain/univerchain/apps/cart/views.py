from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from univerchain.apps.store.models import Product

from .cart import Cart


def cart_summary(request):
    cart = Cart(request)
    context = {"cart": cart, "cart_items": cart.Total_Qty}
    return render(request, "cart/summary.html", context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        if request.user.is_authenticated:
            product_id = int(request.POST.get("productId"))
            product = get_object_or_404(Product, id=product_id)
            cart.add(product)

            response = JsonResponse({"qty": cart.Total_Qty})

            return response
        else:
            return render(request, "cart/add_to_cart_fail.html")


def cart_remove(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = str(request.POST.get("productId"))
        cart.remove(product_id)
        total_price = cart.get_total_price()
        response = JsonResponse({"Success": True, "totalPrice": total_price})

        return response

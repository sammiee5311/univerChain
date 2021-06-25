from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product

from .cart import Cart


def cart_summary(request):
    cart = Cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'store/cart/summary.html', context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        product_qty = int(request.POST.get('productQty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, product_qty)
        total_qty = cart.Total_Qty
        response = JsonResponse({'qty': total_qty})
        return response

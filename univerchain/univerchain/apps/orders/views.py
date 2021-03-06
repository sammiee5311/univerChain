from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from univerchain.apps.cart.cart import Cart
from univerchain.apps.univercoin.ethereum import Ethereum

from .models import Order, OrderItem

ethereum = Ethereum()


@login_required
def add(request):
    cart = Cart(request)

    contract = ethereum.Contract
    ether_state = True if contract else False
    user_id = request.user.id
    user_ethereum_account = request.user.ethereum_account
    total_price = cart.get_total_price()
    order_key = request.POST.get("order_key")
    current_coin = 0

    if ether_state:
        current_coin = contract.functions.balanceOf(user_ethereum_account).call({"from": user_ethereum_account})

    if Order.objects.filter(order_key=order_key).exists() or current_coin < total_price:
        return render(request, "orders/order_fail.html")
    else:
        contract.functions.transfer(ethereum.Owner, int(total_price * 10)).transact({"from": user_ethereum_account})
        order = Order.objects.create(user_id=user_id, total_price=total_price, order_key=order_key)
        order_id = order.pk
        for item in cart:
            OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"])
        cart.clear_session()

    return render(request, "orders/order_success.html")


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(transaction_status=True)
    return orders

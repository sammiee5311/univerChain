from decimal import Decimal

from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    @property
    def Total_Qty(self):
        return len(self.cart)

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.products.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            yield item

    def get_total_price(self):
        total_price = 0

        for item in self.cart.values():
            total_price += Decimal(item['price'])

        return total_price

    def add(self, product):
        product_id = int(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price)}

        self.save_session()

    def remove(self, product_id):
        try:
            del self.cart[product_id]
        except KeyError:
            pass

        self.save_session()

    def save_session(self):
        self.session.modified = True

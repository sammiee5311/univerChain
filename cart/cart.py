from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.products.filter(id__in=product_ids)

    def add(self, product, qty):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price), 'qty': qty}
        else:
            self.cart[product_id]['qty'] = qty

        self.session.modified = True

    @property
    def Total_Qty(self):
        return sum(product['qty'] for product in self.cart.values())

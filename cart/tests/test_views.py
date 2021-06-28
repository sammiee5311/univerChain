from accounts.models import myuser
from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product


class TestCartView(TestCase):
    def setUp(self):
        myuser.objects.create(id=1, username='admin')
        Category.objects.create(id=1, name='book', slug='book')
        Product.objects.create(id=1, category_id=1, title='django book', created_by_id=1,
                               slug='django-book', price=1.5, image='django')
        Product.objects.create(id=2, category_id=1, title='react book', created_by_id=1,
                               slug='react-book', price=2.0, image='django')
        Product.objects.create(id=3, category_id=1, title='djjavascriptango book', created_by_id=1,
                               slug='javascript-book', price=2.0, image='django')
        self.client.post(
            reverse('cart:cart_add'), {'productId': 1, 'action': 'post'}, xhr=True
        )
        self.client.post(
            reverse('cart:cart_add'), {'productId': 2, 'action': 'post'}, xhr=True
        )

    def test_cart_url(self):
        response = self.client.get(reverse('cart:cart_summary'))
        self.assertEqual(response.status_code, 200)

    def test_cart_add(self):
        response = self.client.post(
            reverse('cart:cart_add'), {'productId': 3, 'action': 'post'}, xhr=True
        )
        self.assertEqual(response.json(), {'qty': 3})

    def test_cart_remove(self):
        response = self.client.post(
            reverse('cart:cart_remove'), {'productId': 2, 'action': 'post'}, xhr=True
        )
        self.assertEqual(response.json(), {'Success': True, 'total_price': '1.50'})
        response = self.client.post(
            reverse('cart:cart_remove'), {'productId': 3, 'action': 'post'}, xhr=True
        )
        self.assertEqual(response.json(), {'Success': True, 'total_price': '1.50'})

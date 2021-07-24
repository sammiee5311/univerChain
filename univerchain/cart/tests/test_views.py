from accounts.models import MyUser
from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product


class TestCartView(TestCase):
    def setUp(self):
        self.client_without_login = Client()
        self.user = MyUser.objects.create(id=1, username='admin')
        self.client.force_login(self.user)
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
        response_with_login = self.client.post(
            reverse('cart:cart_add'), {'productId': 3, 'action': 'post'}, xhr=True
        )
        response_without_login = self.client_without_login.post(
            reverse('cart:cart_add'), {'productId': 3, 'action': 'post'}, xhr=True
        )
        self.assertEqual(response_with_login.json(), {'qty': 3})
        self.assertIsNotNone(response_without_login.context['cart'])

    def test_cart_remove(self):
        response = self.client.post(
            reverse('cart:cart_remove'), {'productId': 2, 'action': 'post'}, xhr=True
        )
        self.assertEqual(response.json(), {'Success': True, 'totalPrice': '1.50'})
        response = self.client.post(
            reverse('cart:cart_remove'), {'productId': 3, 'action': 'post'}, xhr=True
        )
        self.assertEqual(response.json(), {'Success': True, 'totalPrice': '1.50'})

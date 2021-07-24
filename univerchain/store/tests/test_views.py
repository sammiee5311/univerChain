from importlib import import_module

from accounts.models import MyUser
from django.conf import settings
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse
from store.models import Category, Product
from store.views import product_all

# from unittest import skip


# @skip("demonstrating skipping")
class TestViewResponses(TestCase):
    def setUp(self):
        self.client = Client()
        MyUser.objects.create(id=1, username='admin')
        Category.objects.create(id=1, name='book', slug='book')
        Product.objects.create(category_id=1, title='django book', created_by_id=1,
                               slug='django-book', price='1.5', image='django')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.client.get('/store/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/', HTTP_HOST='example.com')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/', HTTP_HOST='univerchain.com')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test product detail page response status
        """
        response = self.client.get(reverse('store:product_detail', args=['django-book']))
        self.assertEqual(response.status_code, 200)

    def test_category_url(self):
        """
        Test category page response status
        """
        response = self.client.get(reverse('store:category_list', args=['book']))
        self.assertEqual(response.status_code, 200)

    def test_store_main_page_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title> univerchain  | store  </title>', html)
        self.assertTrue(html.startswith('\n<!doctype html>\n'))
        self.assertEqual(response.status_code, 200)

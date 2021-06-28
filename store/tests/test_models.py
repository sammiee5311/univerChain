from accounts.models import myuser
from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product


class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data = Category.objects.create(id=1, name='book', slug='book')

    def test_category_model_entry(self):
        """
        insertion/types/field attributes test
        """
        data = self.data
        self.assertTrue(isinstance(data, Category))

    def test_category_name(self):
        """
        default name test
        """
        data = self.data
        self.assertEqual(str(data), 'book')


class TestProductsModel(TestCase):
    def setUp(self):
        myuser.objects.create(id=1, username='admin')
        Category.objects.create(id=1, name='book', slug='book')
        self.data = Product.objects.create(category_id=1, title='django book', created_by_id=1,
                                           slug='django-book', price='1.5', image='django')

    def test_products_model_entry(self):
        """
        insertion/types/field attributes test
        """
        data = self.data
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django book')

    def test_products_url(self):
        """
        Test product model slug and URL reverse
        """
        data = self.data
        url = reverse('store:product_detail', args=[data.slug])
        self.assertEqual(url, '/store/django-book')
        response = self.client.post(
            reverse('store:product_detail', args=[data.slug]))
        self.assertEqual(response.status_code, 200)

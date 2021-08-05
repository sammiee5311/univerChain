import datetime

import factory
from django.utils import timezone
from factory.declarations import SubFactory
from faker import Faker
from univerchain.apps.accounts.models import MyUser
from univerchain.apps.attendance.models import Attendance, UniversityClass
from univerchain.apps.orders.models import Order, OrderItem
from univerchain.apps.store.models import (
    Category,
    Product,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)
from univerchain.apps.univercoin.ethereum import Ethereum

fake = Faker()

# Store


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "python"
    slug = "python"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType
        django_get_or_create = ("name",)

    name = "e-book"


class ProductSpecificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    product_type = factory.SubFactory(ProductTypeFactory)
    name = "genre"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_type = factory.SubFactory(ProductTypeFactory)
    category = factory.SubFactory(CategoryFactory)
    title = "test"
    description = fake.text()
    slug = "test"
    regular_price = "1.5"
    discount_price = "1.2"


class ProductSpecificationValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecificationValue

    product = factory.SubFactory(ProductFactory)
    specification = factory.SubFactory(ProductSpecificationFactory)
    value = "programming"


# Accounts


class MyUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MyUser

    email = "test@test.com"
    username = "test"
    name = "test"
    password = "test"
    ethereum_account = "test"
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


# Orders


class OrdersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(MyUserFactory)
    created = timezone.now()
    updated = timezone.now()
    total_price = 1.5
    order_key = "test"
    transaction_status = False


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrdersFactory)
    product = factory.SubFactory(ProductFactory)
    price = 1.5
    quantity = 1


# Attendance


class UniversityClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UniversityClass

    name = "physics"
    date = (3).to_bytes(2, byteorder="big")
    description = "Quantum Theory"
    start_time = datetime.time(9, 0, 0)
    end_time = datetime.time(12, 0, 0)


class AttendanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attendance

    student = factory.SubFactory(MyUserFactory)
    class_name = factory.SubFactory(UniversityClassFactory)
    time = timezone.now()
    is_attended = False
    created = timezone.now()

import factory
from faker import Faker
from univerchain.apps.accounts.models import MyUser
from univerchain.apps.store.models import (
    Category,
    Product,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)

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
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)

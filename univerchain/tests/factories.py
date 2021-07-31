import factory
from faker import Faker
from univerchain.apps.store.models import (
    Category,
    Product,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)

fake = Faker()


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

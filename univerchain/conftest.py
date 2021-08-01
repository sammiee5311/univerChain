import pytest
from pytest_factoryboy import register

from tests.factories import (
    CategoryFactory,
    MyUserFactory,
    ProductFactory,
    ProductSpecificationFactory,
    ProductSpecificationValueFactory,
    ProductTypeFactory,
)

register(CategoryFactory)
register(ProductTypeFactory)
register(ProductSpecificationFactory)
register(ProductFactory)
register(ProductSpecificationValueFactory)
register(MyUserFactory)


@pytest.fixture
def category(db, category_factory):
    category = category_factory.create()
    return category


@pytest.fixture
def product_type(db, product_type_factory):
    product_type = product_type_factory.create()
    return product_type


@pytest.fixture
def product_specification(db, product_specification_factory):
    product_specification = product_specification_factory.create()
    return product_specification


@pytest.fixture
def product(db, product_factory):
    product = product_factory.create()
    return product


@pytest.fixture
def product_specification_value(db, product_specification_value_factory):
    product_specification_value = product_specification_value_factory.create()
    return product_specification_value


@pytest.fixture
def my_user(db, my_user_factory):
    my_user = my_user_factory.create()
    return my_user


@pytest.fixture
def admin_user(db, my_user_factory):
    my_user = my_user_factory.create(username="admin", is_staff=True, is_superuser=True)
    return my_user

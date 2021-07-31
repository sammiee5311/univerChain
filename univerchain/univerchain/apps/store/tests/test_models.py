import pytest
from django.urls import reverse


def test_category_name(category):
    assert str(category) == "python"


def test_category_url(client, category):
    slug = category
    url = reverse("store:category_list", args=[slug])
    response = client.get(url)
    assert str(response.context["category"]) == "python"


def test_product_type_name(product_type):
    assert str(product_type) == "e-book"


def test_product_specification_name(product_specification):
    assert str(product_specification) == "genre"


def test_product_title(product):
    assert str(product) == "test"


def test_product_url(client, product):
    slug = product
    url = reverse("store:product_detail", args=[slug])
    response = client.get(url)
    assert response.status_code == 200


def test_product_specification_value(product_specification_value):
    assert str(product_specification_value) == "programming"

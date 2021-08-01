import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_product_all_page(client):
    url = reverse("store:product_all")
    response = client.get(url)
    assert response.status_code == 200

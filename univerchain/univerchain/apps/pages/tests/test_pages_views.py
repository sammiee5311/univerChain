import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_pages_home_render(client):
    response = client.get(reverse("pages:home"))
    assert response.status_code == 200

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_add_to_order_fail(client, my_user, product):
    user = my_user
    client.force_login(user)
    client.post(reverse("cart:cart_add"), {"productId": 1, "action": "post"}, xhr=True)
    response = client.post(reverse("orders:add"), {"order_key": "test1234"})
    assert response.status_code == 200

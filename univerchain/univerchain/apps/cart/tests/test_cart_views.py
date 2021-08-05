import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_add_item_in_cart_login(client, my_user, product):
    user = my_user
    client.force_login(user)
    response = client.post(reverse("cart:cart_add"), {"productId": 1, "action": "post"}, xhr=True)

    assert response.json() == {"qty": 1}


@pytest.mark.django_db
def test_add_item_in_cart_without_login(client, product):
    response = client.post(reverse("cart:cart_add"), {"productId": 1, "action": "post"}, xhr=True)

    assert response.status_code == 200


@pytest.mark.django_db
def test_summary_cart_render(client, my_user, product):
    user = my_user
    client.force_login(user)
    client.post(reverse("cart:cart_add"), {"productId": 1, "action": "post"}, xhr=True)
    response = client.get(reverse("cart:cart_summary"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_remove_item_in_cart(client, my_user, product):
    user = my_user
    client.force_login(user)
    client.post(reverse("cart:cart_add"), {"productId": 1, "action": "post"}, xhr=True)
    client.post(reverse("cart:cart_remove"), {"productId": 2, "action": "post"}, xhr=True)
    response = client.post(reverse("cart:cart_remove"), {"productId": 1, "action": "post"}, xhr=True)

    assert response.json() == {"Success": True, "totalPrice": 0}

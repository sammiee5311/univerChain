import pytest
from django.urls import reverse
from univerchain.apps.accounts.forms import RegistrationForm

# Registration


@pytest.mark.parametrize(
    "username, email, password, password_confirm, univercoin_account, valid",
    [
        ("user1", "1@1.com", "user1", "user1", "user1", True),
        ("user1", "1@1.com", "user1", "user2", "user1", False),
    ],
)
@pytest.mark.django_db
def test_user_registration(username, email, password, password_confirm, univercoin_account, valid):
    form = RegistrationForm(
        data={
            "username": username,
            "email": email,
            "password": password,
            "password_confirm": password_confirm,
            "univercoin_account": univercoin_account,
        }
    )
    assert form.is_valid() is valid


@pytest.mark.parametrize(
    "username, email, password, password_confirm, univercoin_account, valid",
    [
        ("user1", "1@1.com", "user1", "user1", "user1", 302),
        ("user1", "1@1.com", "user1", "user2", "user1", 400),
    ],
)
@pytest.mark.django_db
def test_user_registration_views(client, username, email, password, password_confirm, univercoin_account, valid):
    response = client.post(
        reverse("accounts:register"),
        data={
            "username": username,
            "email": email,
            "password": password,
            "password_confirm": password_confirm,
            "univercoin_account": univercoin_account,
        },
    )

    assert response.status_code == valid


@pytest.mark.parametrize(
    "username, email, password, password_confirm, univercoin_account", [("user1", "1@1.com", "user1", "user1", "user1")]
)
@pytest.mark.django_db
def test_user_registration_email_activate(client, username, email, password, password_confirm, univercoin_account):
    response = client.post(
        reverse("accounts:register"),
        {
            "username": username,
            "email": email,
            "password": password,
            "password_confirm": password_confirm,
            "univercoin_account": univercoin_account,
        },
    )

    uid = response.context["uid"]
    token = response.context["token"]
    response_email1 = client.post(reverse("accounts:activate", args=[uid, token]))
    response_email2 = client.post(reverse("accounts:activate", args=[uid, "test"]))

    assert response_email1.status_code == 302
    assert response_email2.status_code == 200


def test_user_registration_authenticated(client, my_user):
    user = my_user
    client.force_login(user)
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_registration_render(client):
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200


# Order


def test_user_orders_render(client, my_user):
    user = my_user
    client.force_login(user)
    response = client.get(reverse("accounts:orders"))
    assert response.status_code == 200


# Password Reset
@pytest.mark.parametrize(
    "email, valid",
    [
        ("test@test.com", 302),
    ],
)
@pytest.mark.django_db
def test_user_password_reset(client, my_user, email, valid):
    response = client.post(reverse("accounts:password_reset"), {"email": email})

    uid = response.context["uid"]
    token = response.context["token"]
    response_email = client.post(reverse("accounts:password_reset_confirm", args=[uid, token]))
    assert response_email.status_code == valid


# Edit


def test_user_edit(client, my_user):
    user = my_user
    client.force_login(user)
    response = client.post(reverse("accounts:edit_info"), {"name": "test2", "email": "test@test.com"})
    assert response.context["edit_form"]["email"].value() == "test@test.com"
    assert response.status_code == 200


# Delete


def test_user_delete(client, my_user):
    user = my_user
    client.force_login(user)
    response = client.get(reverse("accounts:delete"))
    assert response.status_code == 302


# Account page


def test_user_account_render(client, my_user):
    user = my_user
    client.force_login(user)
    response = client.get(reverse("accounts:account"))
    assert response.status_code == 200


# Univercoin


def test_user_univercoin_render(client, my_user):
    user = my_user
    client.force_login(user)
    response = client.get(reverse("accounts:univercoin"))
    assert response.status_code == 200

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


# Edit


# Delete


def test_user_registration_authenticated(client, my_user):
    user = my_user
    client.force_login(user)
    response = client.get(reverse("accounts:delete"))
    assert response.status_code == 302

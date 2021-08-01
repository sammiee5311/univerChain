import pytest


def test_user_name(my_user):
    assert str(my_user) == "test"


def test_admin_user_name(admin_user):
    assert str(admin_user) == "admin"


@pytest.mark.xfail(raises=ValueError)
def test_user_without_email_fail(my_user_factory):
    my_user_factory.create(email="")


def test_user_incorrect_email_fail(my_user_factory):
    with pytest.raises(ValueError) as error:
        my_user_factory.create(email="test")
    assert str(error.value) == "You must type a valid email address"


@pytest.mark.xfail(raises=ValueError)
def test_admin_user_email_without_email_fail(my_user_factory):
    my_user_factory.create(email="", is_staff=True, is_superuser=True)


def test_admin_user_incorrect_email_fail(my_user_factory):
    with pytest.raises(ValueError) as error:
        my_user_factory.create(email="test", is_staff=True, is_superuser=True)
    assert str(error.value) == "You must type a valid email address"


@pytest.mark.xfail(raises=ValueError)
def test_admin_user_without_staff_fail(my_user_factory):
    my_user_factory.create(email="test@test.com", is_staff=False, is_superuser=True)


def test_admin_user_incorrect_superuser_fail(my_user_factory):
    with pytest.raises(ValueError) as error:
        my_user_factory.create(email="test@test.com", is_staff=True, is_superuser=False)
    assert str(error.value) == "Wrong Value : is_superuser=False"

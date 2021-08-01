from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models


class CustomAccountManager(BaseUserManager):
    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("You must type a valid email address")

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if "ethereum_account" not in other_fields:
            other_fields.setdefault("ethereum_account", "superuser")

        if email:
            email = self.normalize_email(email)
            self.validate_email(email)
        else:
            raise ValueError("You must type an email address")

        if other_fields.get("is_staff") is not True:
            raise ValueError("Wrong Value : is_staff=False")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Wrong Value : is_superuser=False")

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):
        if email:
            email = self.normalize_email(email)
            self.validate_email(email)
        else:
            raise ValueError("You must type an email address")

        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractUser):
    email = models.EmailField("email address", unique=True)
    username = models.CharField(max_length=150, unique=True)
    ethereum_account = models.CharField(max_length=512, blank=False)
    name = models.CharField(max_length=150, blank=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.username

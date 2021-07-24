from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        ethereum_account = "superuser"

        if other_fields.get("is_staff") is not True:
            raise ValueError("Wrong Value : is_staff=False")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Wrong Value : is_superuser=False")

        return self.create_user(email, username, password, ethereum_account, **other_fields)

    def create_user(self, email, username, password, ethereum_account, **other_fields):
        if not email:
            raise ValueError("You must type an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, ethereum_account=ethereum_account, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractUser):
    email = models.EmailField("email address", unique=True)
    username = models.CharField(max_length=150, unique=True)
    ethereum_account = models.CharField(max_length=512, blank=False)
    first_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.username

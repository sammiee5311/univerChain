from django.contrib.auth.models import AbstractUser
from django.db import models


class myuser(AbstractUser):
    ethereum_account = models.CharField(max_length=512, blank=False)

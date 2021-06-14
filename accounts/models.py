from django.db import models
from django.contrib.auth.models import AbstractUser

class myuser(AbstractUser):
    ethereum_account=models.CharField(max_length=512, blank=False)

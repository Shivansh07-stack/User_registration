# account/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=14, unique=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    address = models.TextField()
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username


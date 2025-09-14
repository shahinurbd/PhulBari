from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


# Create your models here.

class UserAddress(models.Model):
    country = models.TextField(default="Bangladesh",blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='user_address', blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

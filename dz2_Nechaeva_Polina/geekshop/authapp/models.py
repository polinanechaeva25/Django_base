from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    country = models.CharField(verbose_name='страна', max_length=128)
    phone_number = models.CharField(verbose_name='номер телефона', max_length=14)
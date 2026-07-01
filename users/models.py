from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    
    class Meta:
        verbose_name = "Пользоаптель"
        verbose_name_plural= "Пользователи"
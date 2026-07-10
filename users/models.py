from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('buyer', 'Покупатель'),
        ('seller', 'Продавец')
    ]
    
    phone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer', verbose_name="Роль")
    
    class Meta:
        verbose_name = "Пользоаптель"
        verbose_name_plural= "Пользователи"
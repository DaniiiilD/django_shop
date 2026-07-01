from django.contrib import admin
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'is_superuser', 'is_staff']
    list_filter = ["is_superuser", 'is_staff', 'groups']
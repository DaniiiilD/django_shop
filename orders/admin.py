from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'final_sum', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']
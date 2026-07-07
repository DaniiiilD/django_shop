from django.contrib import admin
from .models import Category, Product, Size, ProductImage
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name']
    search_fields = ['name']
    prepopulated_fields = {"slug" : ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug' : ('name',)}
    
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_main']
    list_filter = ['is_main']
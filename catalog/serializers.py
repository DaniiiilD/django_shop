from rest_framework import serializers
from .models import Category, Product, Size, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image' , 'is_main']

class CategorySerializer(serializers.ModelField):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']
        
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only = True)
    sizes = serializers.StringRelatedField(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'category_name',
            'price', 'description', 'stock', 'sizes', 'images',
            'created_at', 'is_active'
        ]
        
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']
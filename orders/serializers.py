from rest_framework import serializers
from .models import Order, OrderItem, Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = OrderItem
        fields = ['id' , 'order', 'product', 'product_name', 'quantity', 'price', 'total_price']
        
class OrderItemCreateSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True)
    )
    quantity = serializers.IntegerField(min_value=1)

    def validate_product(self, value):
        if value.stock < 1:
            raise serializers.ValidationError(f'Товара {value.name} нет на складе')
        return value
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta: 
        model = Order
        fields = [
            'id' , 'user', 'user_username' , 'status', 'created_at', 'updated_at', "final_sum",
            'items'
        ]
        read_only_fields = ['user' , 'user_username', 'final_sum']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True, write_only = True)
    
    class Meta:
        model = Order
        fields = ['id', 'status', 'items', "final_sum", 'created_at']
        
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        order = Order.objects.create(
            user = user,
            status = validated_data.get("status", 'new')
        )
        
        total_sum = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
        
            if quantity > product.stock:
                order.delete()
                raise serializers.ValidationError(
                    f'Товара {product.name} на складе только {product.stock}, а запрошено {quantity}'
                )
            order_item = OrderItem.objects.create(
                order = order,
                product = product,
                quantity=quantity,
                price = product.price
            )
            
            product.stock -= quantity
            product.save()
            
            total_sum += order_item.total_price
            
        order.final_sum = total_sum
        order.save()
        
        return order
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        if self.request.user.role != 'buyer':
            raise PermissionDenied('Только покупатели могут создавать заказы')
        serializer.save(user=self.request.user)
        
class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)
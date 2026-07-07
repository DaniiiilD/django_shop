from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order_items', OrderItemViewSet, basename='order_item')

urlpatterns = [
    path('', include(router.urls)),
]
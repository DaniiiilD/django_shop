from django.db import models
from catalog.models import Product
from django.conf import settings
# Create your models here.frf

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь")
    
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус"
    )
    
    created_at =  models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    final_sum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Итоговая сумма",
    )
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы" 
        ordering = ["-created_at"]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._calculate_total
        
    def _calculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        Order.objects.filter(pk=self.pk).update(final_sum=total)
    
    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ"   
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name = "Товар")
    
    quantity = models.IntegerField(
        default=1,
        verbose_name="Количество"
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places= 2,
        verbose_name="Цена за единицу",
        blank=True,
        null=True)
    
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиция заказов"
        
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
        self.order._calculate_total()
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.price * self.quantity
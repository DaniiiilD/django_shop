from django.db import models
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30, blank=True, verbose_name="Название товара")
    slug = models.SlugField(unique=True, verbose_name="URL-слаг")
    description = models.TextField(max_length=200, blank=True, verbose_name="Описание товара")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        
    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10, verbose_name="Размер")
    
    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name="Название товара")
    slug = models.SlugField(unique=True, verbose_name="URL-слаг")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=False, verbose_name="Описание")
    sizes = models.ManyToManyField(Size, blank=True, verbose_name="Размеры")
    stock = models.IntegerField(default=0, verbose_name="Остаток на скалде")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    def __str__(self):
        return self.name
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images' , verbose_name="Товар")
    image = models.ImageField(upload_to='products/', verbose_name="Главное фото")
    is_main = models.BooleanField(default=False, verbose_name="Главное фото")
    
    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товаров"
        
    def __str__(self):
        return f"Фото для {self.product.name}"
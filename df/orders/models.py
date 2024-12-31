# orders/models.py

import uuid
from django.db import models
from django.conf import settings

from catalog.models import Product



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),

    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=50, default="В обработке")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    unique_key = models.UUIDField(default=uuid.uuid4, unique=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Общая стоимость заказа")

    # Поля для доставки:
    recipient_name = models.CharField(max_length=100, blank=True, verbose_name='Имя получателя')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Телефон')
    address = models.TextField(blank=True, verbose_name='Адрес доставки')
    comment = models.TextField(blank=True, verbose_name='Комментарий к заказу')

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')


    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history', verbose_name='Заказ')
    status = models.CharField(max_length=10, choices=Order.STATUS_CHOICES, verbose_name='Новый статус')
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Используем кастомную модель пользователя или стандартную
        on_delete=models.SET_NULL,  # Или CASCADE, если хотите удалять связанные записи
        null=True,  # Разрешаем NULL, чтобы избежать ошибок
        blank=True
    )
    # - on_delete = models.SET_NULL: если пользователь удалён, запись
    # будет ссылаться на NULL.
    # - on_delete = models.CASCADE: если пользователь удалён, связанные
    # записи также будут удалены.

    def __str__(self):
        return f"Заказ #{self.order.id}: {self.get_status_display()} в {self.changed_at}"

class Meta:
    ordering = ['-created_at']



from django.db import models
from django.conf import settings



class Product(models.Model):

    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    stock = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')  # Поле stock

    def __str__(self):
        return self.name


# class Review(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
#     rating = models.PositiveIntegerField(verbose_name='Рейтинг')
#     comment = models.TextField(blank=True, verbose_name='Отзыв')
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
#
#     def __str__(self):
#         return f"Отзыв на {self.product.name} от {self.user.username}"

class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )  # Связь с пользователем
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар",
        related_name="reviews"
    )  # Связь с товаром
    comment = models.TextField(verbose_name="Отзыв")  # Поле для текста отзыва
    rating = models.PositiveSmallIntegerField(
        verbose_name="Рейтинг",
        choices=[(i, f"{i} звёзд{'а' if i == 1 else ''}") for i in range(1, 6)]
    )  # Рейтинг от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # Дата создания отзыва

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.product.name}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]  # Сортировка по дате создания, сначала новые

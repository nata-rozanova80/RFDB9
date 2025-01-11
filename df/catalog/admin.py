from django.contrib import admin
from .models import Product, Review   #Order, OrderItem

admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(OrderItem)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating', 'created_at')  # Поля для отображения в списке
    list_filter = ('rating', 'created_at')  # Возможность фильтрации
    search_fields = ('user__username', 'product__name', 'comment')  # Поля для поиска
    ordering = ('-created_at',)

admin.site.register(Review, ReviewAdmin)

# catalog/urls.py
from django.urls import path
from .views import product_list
from .views import view_cart, add_to_cart
from .views import index

urlpatterns = [

    path('', product_list, name='product_list'),  # Список продуктов

# Другие маршруты...
    path('add-to-cart/', add_to_cart, name='add_to_cart'), #-    старый маршрут
    #path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
]




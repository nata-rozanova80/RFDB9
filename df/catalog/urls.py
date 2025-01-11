# catalog/urls.py
from django.urls import path
from . import views
from .views import product_list, add_review
from .views import view_cart, add_to_cart


urlpatterns = [

    path('', product_list, name='product_list'),  # Список продуктов

# Другие маршруты...
    path('add-to-cart/', add_to_cart, name='add_to_cart'), #-    старый маршрут
    #path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('product/<int:product_id>/add_review/', add_review, name='add_review'),

]




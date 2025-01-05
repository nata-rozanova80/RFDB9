# orders/urls.py

from django.urls import path
from . import views
from .views import checkout
from .views import order_list
from .views import update_order_status # 2-1-6 из 27.12 Q&A


urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('update/<int:order_id>/', views.order_update, name='order_update'),  # Страница обновления статуса заказа
    path('orders/', order_list, name='order_list'),
    path('analytics/', views.analytics_report, name='analytics_report'),
    path('report/', views.order_report, name='order_report'),  # Отчет по заказам
    path('analytics/export/csv/', views.export_analytics_csv, name='export_analytics_csv'),  # Экспорт CSV
    path("update_order/<int:order_id>/", update_order_status, name="update_order_status"),
]




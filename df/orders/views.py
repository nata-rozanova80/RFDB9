# orders/views.py
import requests
from django.http import JsonResponse

import csv
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .models import Product
from .models import Order, OrderItem
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from django.shortcuts import redirect, get_object_or_404
from .forms import OrderStatusForm

from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import timedelta

from django.core.paginator import Paginator
from django.db.models import Q


def order_success(request, order_id):
    # Получаем объект заказа по его ID
    order = Order.objects.get(id=order_id)

    # Передаем `unique_key` из объекта заказа в шаблон
    return render(request, 'orders/order_success.html', {'unique_key': order.unique_key})

# Код из 27.12 ответы на вопросы
def update_order_status(request, order_id):
    # Пример данных для отправки
    unique_key = "example_key"
    status = "Обновлен"
    webhook_url = "http://127.0.0.1:8001/webhook"

    try:
        response = requests.post(webhook_url, json={"order_id": order_id, "status": status})
        if response.status_code == 200:
            return JsonResponse({"success": "Notification sent to bot"})
        else:
            return JsonResponse({"error": "Failed to send notification"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Ваша корзина пуста! Добавьте товары, прежде чем оформлять заказ.")
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Сохраняем заказ
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = 0  # Инициализация общей суммы заказа
            order.save()

            # Добавляем товары из корзины в заказ
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                price_for_quantity = product.price * quantity  # Умножение количества на цену
                OrderItem.objects.create(order=order, product=product, quantity=quantity)

                # Увеличиваем общую стоимость заказа
                order.total_price += price_for_quantity

            # Сохраняем обновлённую общую сумму заказа
            order.save()

            # Очищаем корзину
            request.session['cart'] = {}

            # Передаём сообщение с ключом заказа
            messages.success(request,
                             f"Заказ успешно оформлен! Код вашего заказа: {order.unique_key}. Мы свяжемся с вами для подтверждения.")

            # Перенаправляем на страницу успеха с ключом заказа
            return redirect('order_success', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'orders/checkout.html', {'form': form})


# Проверка, что пользователь является администратором
def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

@user_passes_test(is_admin)
def order_update(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'orders/order_update.html', {'form': form, 'order': order})

@user_passes_test(is_admin)
def analytics_report(request):
    # Пример оптимизации
    popular_products = OrderItem.objects.select_related('product').values('product__name').annotate(
        total_sold=Sum('quantity')).order_by('-total_sold')[:10]

    # Общий объем продаж
    total_sales = OrderItem.objects.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0

    # Количество проданных товаров
    total_products_sold = OrderItem.objects.aggregate(total=Sum('quantity'))['total'] or 0

    # Самые популярные товары
    popular_products = OrderItem.objects.values('product__name').annotate(total_sold=Sum('quantity')).order_by('-total_sold')[:10]

    # Доход по статусам заказов
    revenue_by_status = OrderItem.objects.values('order__status').annotate(total=Sum(F('product__price') * F('quantity'))).order_by('-total')

    # Количество заказов по дням за последний месяц
    today = timezone.now()
    last_month = today - timedelta(days=30)
    orders_last_month = Order.objects.filter(created_at__gte=last_month)
    orders_by_day = orders_last_month.extra({'day': "date(created_at)"}).values('day').annotate(count=Count('id')).order_by('day')

    context = {
        'total_sales': total_sales,
        'total_products_sold': total_products_sold,
        'popular_products': popular_products,
        'revenue_by_status': revenue_by_status,
        'orders_by_day': orders_by_day,
    }

    return render(request, 'orders/analytics_report.html', context)


@user_passes_test(is_admin)
def order_report(request):
    orders = Order.objects.select_related('user').prefetch_related('items__product').all()

    # Фильтрация
    status_filter = request.GET.get('status')
    user_filter = request.GET.get('user')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if status_filter and status_filter != 'all':
        orders = orders.filter(status=status_filter)

    if user_filter:
        orders = orders.filter(user__username__icontains=user_filter)

    if date_from:
        orders = orders.filter(created_at__date__gte=date_from)

    if date_to:
        orders = orders.filter(created_at__date__lte=date_to)

    # Сортировка
    sort_by = request.GET.get('sort', '-created_at')
    orders = orders.order_by(sort_by)

    # Пагинация
    paginator = Paginator(orders, 20)  # 20 заказов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Статусы для фильтрации
    statuses = Order.STATUS_CHOICES

    context = {
        'page_obj': page_obj,
        'statuses': statuses,
        'current_status': status_filter or 'all',
        'current_user': user_filter or '',
        'date_from': date_from or '',
        'date_to': date_to or '',
        'sort_by': sort_by,
        'orders': orders,
    }

    return render(request, 'orders/order_report.html', context)

@user_passes_test(is_admin)
def export_analytics_csv(request):
    # Получаем данные аналогично аналитическому отчету
    total_sales = OrderItem.objects.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0
    total_products_sold = OrderItem.objects.aggregate(total=Sum('quantity'))['total'] or 0
    popular_products = OrderItem.objects.values('product__name').annotate(total_sold=Sum('quantity')).order_by('-total_sold')[:10]
    revenue_by_status = OrderItem.objects.values('order__status').annotate(total=Sum(F('product__price') * F('quantity'))).order_by('-total')
    today = timezone.now()
    last_month = today - timedelta(days=30)
    orders_last_month = Order.objects.filter(created_at__gte=last_month)
    orders_by_day = orders_last_month.extra({'day': "date(created_at)"}).values('day').annotate(count=Count('id')).order_by('day')

    # Создаем HTTP-ответ с заголовками для скачивания файла
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="analytics_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Показатель', 'Значение'])

    writer.writerow(['Общий объем продаж', total_sales])
    writer.writerow(['Количество проданных товаров', total_products_sold])

    writer.writerow([])
    writer.writerow(['Самые популярные товары', 'Количество проданных шт.'])
    for product in popular_products:
        writer.writerow([product['product__name'], product['total_sold']])

    writer.writerow([])
    writer.writerow(['Доход по статусам заказов', 'Доход (руб.)'])
    for status in revenue_by_status:
        writer.writerow([status['order__status'].capitalize(), status['total']])

    writer.writerow([])
    writer.writerow(['Количество заказов по дням (последний месяц)', 'Количество заказов'])
    for order in orders_by_day:
        writer.writerow([order['day'], order['count']])

    return response





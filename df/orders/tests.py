from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product
from .models import Order, OrderItem

class OrderModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя и продукт
        self.user = User.objects.create_user(username="testuser", password="password")
        self.product = Product.objects.create(name="Тестовый букет", price=1000.00)
        self.order = Order.objects.create(user=self.user, status="pending")

    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, "pending")

    def test_order_str_method(self):
        self.assertEqual(str(self.order), f"Заказ #{self.order.id} от {self.order.user.username}")

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.product = Product.objects.create(name="Тестовый букет", price=1000.00)
        self.order = Order.objects.create(user=self.user, status="pending")
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)

    def test_order_total_price(self):
        self.assertEqual(self.order_item.quantity * self.product.price, 2000.00)

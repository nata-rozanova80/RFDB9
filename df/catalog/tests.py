from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, Review

class ProductModelTest(TestCase):
    def setUp(self):
        # Создаем тестовый продукт
        self.product = Product.objects.create(
            name="Тестовый букет",
            description="Описание тестового букета",
            price=1000.00
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Тестовый букет")
        self.assertEqual(self.product.price, 1000.00)
        self.assertEqual(self.product.description, "Описание тестового букета")

    def test_product_str_method(self):
        self.assertEqual(str(self.product), "Тестовый букет")

class ReviewModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя и продукт
        self.user = User.objects.create_user(username="testuser", password="password")
        self.product = Product.objects.create(name="Тестовый букет", price=1000.00)
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Отличный букет!"
        )

    def test_review_creation(self):
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "Отличный букет!")

    def test_review_str_method(self):
        self.assertEqual(
            str(self.review),
            f"Отзыв от {self.review.user.username} о {self.review.product.name}"
        )

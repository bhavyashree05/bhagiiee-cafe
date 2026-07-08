from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from .models import CoffeeItem
from .utils import (
    InsufficientPaymentError,
    InsufficientStockError,
    calculate_change,
    calculate_order_total,
    deduct_stock,
    has_sufficient_stock,
)


class CalculationTests(TestCase):
    def test_calculate_order_total(self):
        self.assertEqual(calculate_order_total(Decimal("50.00"), 3), Decimal("150.00"))

    def test_calculate_change_exact(self):
        self.assertEqual(calculate_change(Decimal("100.00"), Decimal("100.00")), Decimal("0.00"))

    def test_calculate_change_with_extra(self):
        self.assertEqual(calculate_change(Decimal("90.00"), Decimal("100.00")), Decimal("10.00"))

    def test_calculate_change_insufficient_raises(self):
        with self.assertRaises(InsufficientPaymentError):
            calculate_change(Decimal("100.00"), Decimal("50.00"))


class StockTests(TestCase):
    def setUp(self):
        self.item = CoffeeItem.objects.create(name="Latte", price=Decimal("120.00"), stock=5)

    def test_has_sufficient_stock(self):
        self.assertTrue(has_sufficient_stock(self.item, 5))
        self.assertFalse(has_sufficient_stock(self.item, 6))

    def test_deduct_stock_reduces_quantity(self):
        deduct_stock(self.item, 2)
        self.item.refresh_from_db()
        self.assertEqual(self.item.stock, 3)

    def test_deduct_stock_raises_when_insufficient(self):
        with self.assertRaises(InsufficientStockError):
            deduct_stock(self.item, 10)


class ViewAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="testpass123")

    def test_menu_requires_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)  # redirected to login

    def test_menu_accessible_when_logged_in(self):
        self.client.login(username="alice", password="testpass123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

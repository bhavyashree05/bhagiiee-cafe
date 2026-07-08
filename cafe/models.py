from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Profile(models.Model):
    """Extra info attached to Django's built-in User model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"


class CoffeeItem(models.Model):
    """A single item on the coffee menu, e.g. Espresso, Latte."""

    CATEGORY_CHOICES = [
    ("HOT", "Hot Coffee"),
    ("COLD", "Cold Coffee"),
    ("SNACK", "Snacks"),
]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
    max_length=10,
    choices=CATEGORY_CHOICES,
    default="HOT",
)
    description = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    stock = models.PositiveIntegerField(default=0, help_text="Cups/servings currently available")
    image = models.ImageField(upload_to="coffee_images/", blank=True, null=True)
    is_active = models.BooleanField(
        default=True, help_text="Untick to hide this item from the menu without deleting it"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (₹{self.price})"

    @property
    def in_stock(self):
        return self.stock > 0
    @property
    def low_stock(self):
        return self.stock <= 5

    @property
    def is_available(self):
        return self.is_active and self.in_stock


class Order(models.Model):
    """One customer order, e.g. '2 x Latte'."""

    STATUS_PENDING = "PENDING"
    STATUS_PAID = "PAID"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending Payment"),
        (STATUS_PAID, "Paid"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    coffee_item = models.ForeignKey(
        CoffeeItem, on_delete=models.PROTECT, related_name="orders"
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}: {self.quantity} x {self.coffee_item.name}"

    @property
    def total_amount(self):
        """Total price owed for this order (quantity x unit price)."""
        return self.unit_price * self.quantity


class Payment(models.Model):
    """Records the cash payment made against an order and the change given."""

    PAYMENT_CHOICES = [
    ("CASH", "Cash"),
    ("CARD", "Card"),
    ("UPI", "UPI"),
]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    change_returned = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(
    max_length=10,
    choices=PAYMENT_CHOICES,
    default="CASH",
)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order_id}: ₹{self.amount_paid}"

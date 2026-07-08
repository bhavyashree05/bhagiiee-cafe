"""
User-defined helper functions for the coffee machine's business logic.

Keeping this logic in plain functions (instead of burying it inside
views) makes it independently testable and reusable, and is the
"user defined functions" layer of the application: everything that
decides prices, change, stock and sales figures lives here.
"""

from decimal import Decimal

from django.db.models import Sum, F


class InsufficientStockError(Exception):
    """Raised when an order requests more units than are in stock."""


class InsufficientPaymentError(Exception):
    """Raised when the cash tendered is less than the amount owed."""


def calculate_order_total(unit_price, quantity):
    """Return the total price owed for a given unit price and quantity."""
    return Decimal(unit_price) * quantity


def calculate_change(total_due, amount_paid):
    """
    Return the change to give back to the customer.

    Raises InsufficientPaymentError if the amount paid is less than
    the total due, matching real vending-machine behaviour.
    """
    total_due = Decimal(total_due)
    amount_paid = Decimal(amount_paid)

    if amount_paid < total_due:
        raise InsufficientPaymentError(
            f"Amount paid (₹{amount_paid}) is less than the amount due (₹{total_due})."
        )
    return amount_paid - total_due


def has_sufficient_stock(coffee_item, quantity):
    """Return True if the machine has enough beans/cups left for this order."""
    return coffee_item.stock >= quantity


def deduct_stock(coffee_item, quantity):
    """
    Deduct `quantity` units from a CoffeeItem's stock and persist it.

    Raises InsufficientStockError instead of allowing stock to go negative.
    """
    if not has_sufficient_stock(coffee_item, quantity):
        raise InsufficientStockError(
            f"Only {coffee_item.stock} unit(s) of {coffee_item.name} left in stock."
        )
    coffee_item.stock -= quantity
    coffee_item.save(update_fields=["stock"])
    return coffee_item.stock


def restock_item(coffee_item, quantity):
    """Add `quantity` units back to a CoffeeItem's stock (admin restocking)."""
    coffee_item.stock += quantity
    coffee_item.save(update_fields=["stock"])
    return coffee_item.stock


def get_sales_summary():
    """
    Build a small analytics summary used by the admin dashboard:
    total revenue, number of paid orders, and best-selling items.
    """
    from .models import Order  # local import avoids circular import at module load

    paid_orders = Order.objects.filter(status=Order.STATUS_PAID)

    total_orders = paid_orders.count()
    total_revenue = sum((order.total_amount for order in paid_orders), Decimal("0.00"))

    top_items = (
        paid_orders.values("coffee_item__name")
        .annotate(units_sold=Sum("quantity"), revenue=Sum(F("unit_price") * F("quantity")))
        .order_by("-units_sold")[:5]
    )

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "top_items": list(top_items),
    }


def get_low_stock_items(threshold=5):
    """Return CoffeeItems at or below the given stock threshold (for restock alerts)."""
    from .models import CoffeeItem

    return CoffeeItem.objects.filter(stock__lte=threshold, is_active=True).order_by("stock")

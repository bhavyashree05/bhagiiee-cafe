from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import OrderQuantityForm, PaymentForm, RegisterForm
from .models import CoffeeItem, Order, Payment
from .utils import (
    InsufficientPaymentError,
    InsufficientStockError,
    calculate_change,
    calculate_order_total,
    deduct_stock,
    get_low_stock_items,
    get_sales_summary,
)


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


# --------------------------------------------------------------------------
# Auth: register / login / logout
# --------------------------------------------------------------------------
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account was created.")
            return redirect("menu")
    else:
        form = RegisterForm()
    return render(request, "cafe/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("menu")
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "cafe/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


# --------------------------------------------------------------------------
# Menu & ordering
# --------------------------------------------------------------------------
@login_required
def menu(request):
    items = CoffeeItem.objects.filter(is_active=True)
    return render(request, "cafe/menu.html", {"items": items})


@login_required
def place_order(request, item_id):
    coffee_item = get_object_or_404(CoffeeItem, pk=item_id, is_active=True)

    if request.method == "POST":
        form = OrderQuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            if quantity > coffee_item.stock:
                messages.error(
                    request,
                    f"Sorry, only {coffee_item.stock} unit(s) of {coffee_item.name} left.",
                )
                return redirect("menu")

            order = Order.objects.create(
                user=request.user,
                coffee_item=coffee_item,
                quantity=quantity,
                unit_price=coffee_item.price,
                status=Order.STATUS_PENDING,
            )
            return redirect("payment", order_id=order.pk)
    else:
        form = OrderQuantityForm()

    return render(request, "cafe/order_quantity.html", {"form": form, "item": coffee_item})


@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if order.status == Order.STATUS_PAID:
        return redirect("receipt", order_id=order.pk)

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount_paid = form.cleaned_data["amount_paid"]
            try:
                change = calculate_change(order.total_amount, amount_paid)
                deduct_stock(order.coffee_item, order.quantity)
            except InsufficientPaymentError as exc:
                messages.error(request, str(exc))
                return render(request, "cafe/payment.html", {"order": order, "form": form})
            except InsufficientStockError as exc:
                messages.error(request, str(exc))
                return redirect("menu")

            Payment.objects.create(
                order=order, amount_paid=amount_paid, change_returned=change
            )
            order.status = Order.STATUS_PAID
            order.save(update_fields=["status"])
            return redirect("receipt", order_id=order.pk)
    else:
        form = PaymentForm()

    return render(request, "cafe/payment.html", {"order": order, "form": form})


@login_required
def receipt(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user, status=Order.STATUS_PAID)
    return render(request, "cafe/receipt.html", {"order": order, "payment": order.payment})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).select_related("coffee_item", "payment")
    return render(request, "cafe/order_history.html", {"orders": orders})


# --------------------------------------------------------------------------
# Admin dashboard (staff only) - sits alongside Django's built-in /admin/
# --------------------------------------------------------------------------
@user_passes_test(is_staff_user, login_url="login")
def admin_dashboard(request):
    summary = get_sales_summary()
    low_stock_items = get_low_stock_items()
    recent_orders = Order.objects.select_related("user", "coffee_item").all()[:10]

    context = {
        "summary": summary,
        "low_stock_items": low_stock_items,
        "recent_orders": recent_orders,
    }
    return render(request, "cafe/dashboard.html", context)
def home(request):
    return render(request, "cafe/home.html")
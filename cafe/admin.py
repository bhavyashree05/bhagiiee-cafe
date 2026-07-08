from django.contrib import admin

from .models import CoffeeItem, Order, Payment, Profile


@admin.register(CoffeeItem)
class CoffeeItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "is_active", "in_stock")
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("price", "stock", "is_active")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "coffee_item", "quantity", "unit_price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "coffee_item__name")
    readonly_fields = ("unit_price", "created_at")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "amount_paid", "change_returned", "paid_at")
    readonly_fields = ("paid_at",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")

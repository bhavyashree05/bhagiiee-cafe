import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CoffeeItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.CharField(blank=True, max_length=255)),
                ("price", models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal("0.00"))])),
                ("stock", models.PositiveIntegerField(default=0, help_text="Cups/servings currently available")),
                ("image", models.ImageField(blank=True, null=True, upload_to="coffee_images/")),
                ("is_active", models.BooleanField(default=True, help_text="Untick to hide this item from the menu without deleting it")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone_number", models.CharField(blank=True, max_length=15)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=6)),
                ("status", models.CharField(choices=[("PENDING", "Pending Payment"), ("PAID", "Paid"), ("CANCELLED", "Cancelled")], default="PENDING", max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("coffee_item", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orders", to="cafe.coffeeitem")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="orders", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount_paid", models.DecimalField(decimal_places=2, max_digits=8)),
                ("change_returned", models.DecimalField(decimal_places=2, max_digits=8)),
                ("paid_at", models.DateTimeField(auto_now_add=True)),
                ("order", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="payment", to="cafe.order")),
            ],
        ),
    ]

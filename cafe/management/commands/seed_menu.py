import shutil
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from cafe.models import CoffeeItem

# (name, description, price, stock, category, image filename in cafe/static/cafe/images/)
STARTER_MENU = [
    ("Espresso", "Bold and concentrated shot", 80, 25, "HOT", "espresso.png"),
    ("Americano", "Espresso with hot water", 90, 20, "HOT", "americano.png"),
    ("Latte", "Espresso with steamed milk", 120, 15, "HOT", "latte.png"),
    ("Cappuccino", "Espresso with steamed milk foam", 120, 15, "HOT", "cappuccino.png"),
    ("Mocha", "Espresso with chocolate and milk", 140, 10, "HOT", "mocha.png"),
    ("Cold Coffee", "Chilled and creamy, served over ice", 130, 12, "COLD", "cold_coffee.png"),
    ("Iced Mocha", "Chocolatey espresso over ice with milk", 150, 10, "COLD", "iced_mocha.png"),
    ("Caramel Frappe", "Blended iced coffee with caramel drizzle", 160, 8, "COLD", "caramel_frappe.png"),
]

STATIC_IMAGE_DIR = Path(__file__).resolve().parents[2] / "static" / "cafe" / "images"


class Command(BaseCommand):
    help = "Seed the database with a starter coffee menu, using the provided product photos."

    def handle(self, *args, **options):
        created_count = 0
        updated_images = 0

        for name, description, price, stock, category, image_filename in STARTER_MENU:
            item, created = CoffeeItem.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                    "price": price,
                    "stock": stock,
                    "category": category,
                },
            )
            if created:
                created_count += 1

            if not item.image:
                source_path = STATIC_IMAGE_DIR / image_filename
                if source_path.exists():
                    with open(source_path, "rb") as image_file:
                        item.image.save(image_filename, File(image_file), save=True)
                    updated_images += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Image not found for {name}: {source_path}")
                    )

        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} new coffee item(s)."))
        self.stdout.write(self.style.SUCCESS(f"Attached images to {updated_images} item(s)."))

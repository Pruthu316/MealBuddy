from django.core.management.base import BaseCommand
from django.core.management import call_command
from delivery.models import Restaurant, Item


class Command(BaseCommand):
    help = 'Seeds initial catalog (restaurants and menu items) if catalog is incomplete or empty.'

    def handle(self, *args, **options):
        restaurant_count = Restaurant.objects.count()
        item_count = Item.objects.count()

        if restaurant_count < 3 or item_count == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Catalog incomplete (Restaurants: {restaurant_count}, Items: {item_count}). Loading catalog seed..."
                )
            )
            call_command('loaddata', 'delivery/fixtures/catalog_seed.json')
            self.stdout.write(self.style.SUCCESS("Catalog seeded successfully."))
        else:
            self.stdout.write(
                self.style.NOTICE(
                    f"Restaurants ({restaurant_count}) and Items ({item_count}) already exist. Skipping catalog seed."
                )
            )

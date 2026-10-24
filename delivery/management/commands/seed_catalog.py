from django.core.management.base import BaseCommand
from django.core.management import call_command
from delivery.models import Restaurant


class Command(BaseCommand):
    help = 'Seeds initial catalog (restaurants and menu items) if database is empty.'

    def handle(self, *args, **options):
        if Restaurant.objects.count() == 0:
            self.stdout.write(self.style.SUCCESS("No restaurants found. Loading catalog seed..."))
            call_command('loaddata', 'delivery/fixtures/catalog_seed.json')
            self.stdout.write(self.style.SUCCESS("Catalog seeded successfully."))
        else:
            self.stdout.write(self.style.NOTICE("Restaurants already exist. Skipping catalog seed."))

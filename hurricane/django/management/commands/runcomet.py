from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Starts a lightweight Comet server for development."

    def handle(self, *args, **options):
        from hurricane.runner import main
        main(settings)

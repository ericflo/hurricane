from django.core.management.base import BaseCommand
from django.conf import settings

from hurricane.runner import main


class Command(BaseCommand):
    help = "Starts a lightweight Comet server for development."

    def handle(self, *args, **options):
        main(settings)

from django.core.management.base import BaseCommand
from django.conf import settings

from hurricane.runner import main

class Command(BaseCommand):
    help = "Starts hurricane"

    def handle(self, *args, **options):
        main(settings)
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Automatically runs makemigrations and migrate commands.'

    def handle(self, *args, **options):
        # Run makemigrations
        call_command('makemigrations')

        # Run migrate
        call_command('migrate')
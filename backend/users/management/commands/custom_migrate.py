from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Automatically runs makemigrations and migrate commands.'

    def handle(self, *args, **options):
        # Run makemigrations
        call_command('makemigrations')

        # Run migrate
        call_command('migrate')
        try:
            User.objects.get(username='admin')
        except:
            admin = User.objects.create(username='admin', email='admin@admin.com', is_superuser=True, is_staff=True, is_active=True)
            admin.set_password('admin')
            admin.save()

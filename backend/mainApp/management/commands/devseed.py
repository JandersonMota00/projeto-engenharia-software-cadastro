from django.core.management.base import BaseCommand
from mainApp import models
from django.core.management import call_command
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Semeia alguns dados no banco de dados para DESENVOLVIMENTO'

    def handle(self, *args, **kwargs):

        call_command('seed')

        User.objects.create_superuser(

            username='admin',

            email='admin@example.com',

            password='adminpassword'

        )

        pass

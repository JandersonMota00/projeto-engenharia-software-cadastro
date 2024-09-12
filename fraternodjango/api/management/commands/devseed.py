from django.core.management.base import BaseCommand
from api import models
from django.core.management import call_command
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class Command(BaseCommand):
    help = 'Semeia alguns dados no banco de dados para DESENVOLVIMENTO'

    def handle(self, *args, **kwargs):

        call_command('seed')

        User.objects.create_superuser(

            username='admin',

            email='admin@example.com',

            password='adminpassword'

        )
        a = models.SelectValue._meta.permissions
        print(a)
        content_type = ContentType.objects.get_for_model(models.SelectValue)
        print(Permission.objects.filter(content_type=content_type))
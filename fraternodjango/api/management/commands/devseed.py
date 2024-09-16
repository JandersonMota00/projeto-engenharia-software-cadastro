from django.core.management.base import BaseCommand
from api import models
from django.core.management import call_command
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class Command(BaseCommand):
    help = 'Semeia alguns dados no banco de dados para DESENVOLVIMENTO'

    def handle(self, *args, **kwargs):

        # Executa comandos de reinicialização e configuração
        
        self.stdout.write(f'=============================================================================================')
        call_command('flush', interactive=False)
        self.stdout.write(self.style.SUCCESS(f'Banco de dados apagado'))
        
        
        self.stdout.write(f'=============================================================================================')
        call_command('removemigrations')
        
        self.stdout.write(f'=============================================================================================')

        self.stdout.write('Criando novas migrações...')

        call_command('makemigrations', 'api')

        self.stdout.write(f'=============================================================================================')

        self.stdout.write('Aplicando migrações...')

        call_command('migrate')

        self.stdout.write(f'=============================================================================================')

        call_command('configpermissions')

        self.stdout.write(f'=============================================================================================')

        call_command('seed')

        User.objects.create_superuser(

            username='admin',

            email='admin@example.com',

            password='adminpassword'

        )


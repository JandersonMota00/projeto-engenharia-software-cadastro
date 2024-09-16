from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Reinicia o banco de dados, exclui migrações e aplica um migração inicial limpa'

    def handle(self, *args, **kwargs):

        # Apaga todas as migrations
        # Não existe um comando cli que faça isso, então lozalizamos e apagamos os arquivos diretamente
        
        self.stdout.write(self.style.NOTICE(f'Apagando migrations'))

        migrations_dir = os.path.join('api', 'migrations')
        for filename in os.listdir(migrations_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                file_path = os.path.join(migrations_dir, filename)
                self.stdout.write(f'Arquivo de migração deletado: {filename}')
                os.remove(file_path)
                
        self.stdout.write(self.style.SUCCESS(f'Migrations apagadas'))
        

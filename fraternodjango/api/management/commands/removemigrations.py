from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Reinicia o banco de dados, exclui migrações dos apps api e selectvalues e aplica uma migração inicial limpa'

    def handle(self, *args, **kwargs):

        apps = ['api', 'selectvalues']
        
        for app in apps:
            self.stdout.write(self.style.NOTICE(f'Apagando migrations do app {app}'))
            migrations_dir = os.path.join(app, 'migrations')
            
            for filename in os.listdir(migrations_dir):
                if filename.endswith('.py') and filename != '__init__.py':
                    file_path = os.path.join(migrations_dir, filename)
                    self.stdout.write(f'Arquivo de migração deletado: {filename}')
                    os.remove(file_path)
                    
        self.stdout.write(self.style.SUCCESS('Migrations apagadas'))

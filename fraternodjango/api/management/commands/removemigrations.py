from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Reinicia o banco de dados, exclui migrações e aplica um migração inicial limpa'

    def handle(self, *args, **kwargs):
        # Apaga o banco de dados atual
        # a função call_command chama um comando cli django
        # para obter a lista das funções execute: python manage.py
        self.stdout.write('Limpando o banco de dados...')
        # comando cli flush apaga o banco de dados
        call_command('flush', verbosity=0, interactive=False)

        # Apaga todas as migrations
        # Não existe um comando cli que faça isso, então lozalizamos e apagamos os arquivos diretamente
        migrations_dir = os.path.join('api', 'migrations')
        for filename in os.listdir(migrations_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                file_path = os.path.join(migrations_dir, filename)
                self.stdout.write(f'Arquivo de migração deletado: {filename}')
                os.remove(file_path)

        self.stdout.write('Criando novas migrações...')
        call_command('makemigrations', 'api')

        self.stdout.write('Aplicando migrações...')
        call_command('migrate')


        self.stdout.write(
            'Banco de dados reiniciado e migrações aplicadas com sucesso.')

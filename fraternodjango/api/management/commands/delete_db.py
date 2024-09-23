# myapp/management/commands/delete_db.py

from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Remove o arquivo db.sqlite3 do diretório raiz do projeto'

    def handle(self, *args, **kwargs):
        db_path = 'db.sqlite3'
        if os.path.exists(db_path):
            os.remove(db_path)
            self.stdout.write(self.style.SUCCESS(f'Arquivo {db_path} removido com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING(f'O arquivo {db_path} não foi encontrado.'))

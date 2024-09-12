from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

#  Sempre que queremos modificar o esquema de tabelas/colunas de um banco de dados
#  precisamos criar uma cosia chama migration, que modifica o banco de dados,
#  e converte todos os dados do formato antigo para o novo

# No django, sempre que alteramos um arquivo models.py, estamos modificando o esquema
# do nosso db. Para criarmos a migration, no caso do Django executamos:
#     python manage.py makemigrations [appname]
# Ao executar esse comando o django tenta criar essa migration de forma automatica,
# semi-automatica (o django pode fazer algumas perguntas no console ao executar o comando

# Entretando, como ainda não temos dados, não precisamos nos preocupar em ter
# uma migration para cada alteração dos models, em vez disso, para cada alteração
# no models iremos executar esse comando que ira fazer o seguinte:

# Apague o banco de Dados
# Apague as migrations ja criadas
# Crie a migration inicial novamente
# Crie o banco de dados



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

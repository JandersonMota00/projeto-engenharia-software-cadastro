# myapp/management/commands/setup_groups_and_permissions.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Cria grupos e permissões para o aplicativo'

    def handle(self, *args, **kwargs):

        group_paciente, created = Group.objects.get_or_create(name='Paciente')
        group_atendente, created = Group.objects.get_or_create(name='Atendente')
        group_diretor, created = Group.objects.get_or_create(name='Diretor')
             
        User_content_type = ContentType.objects.get_for_model(User)
             
        can_register_paciente = Permission.objects.create(
            codename='can_register_paciente',
            name='Pode registrar pacientes',
            content_type=User_content_type,
        )

        can_register_atendente = Permission.objects.create(
            codename='can_register_atendente',
            name='Pode registrar atendentes',
            content_type=User_content_type,
        )

        can_register_diretor = Permission.objects.create(
            codename='can_register_diretor',
            name='Pode registrar diretores',
            content_type=User_content_type,
        )
    


        # Atribuição de Permissões aos Grupos
        group_paciente.permissions.set([
            Permission.objects.get(codename='can_view_only_enableds_state'),
            Permission.objects.get(codename='can_create_only_with_tocheck_state'),
        ])

        group_atendente.permissions.set([
            Permission.objects.get(codename='can_view_all_states'),
            Permission.objects.get(codename='can_view_all_states')
        ])

        group_diretor.permissions.set([
            can_register_atendente,
            can_register_diretor,
            Permission.objects.get(codename='can_view_realname_and_pseudonym')
        ])

        self.stdout.write(self.style.SUCCESS('Grupos e permissões configurados com sucesso.'))

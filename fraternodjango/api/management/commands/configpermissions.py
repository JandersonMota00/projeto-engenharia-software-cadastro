from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from api.models import PermissionContentType

class Command(BaseCommand):
    help = 'Cria grupos e permissões para o aplicativo'

    def handle(self, *args, **kwargs):
        # Define as permissões e os grupos associados
        permissions = {
            
            'can_manage_user_self': ['Paciente', 'Atendente', 'Diretor'],
            # can_manager_user_all'
            
            'can_create_paciente_self':      ['Paciente'],
            'can_create_paciente_any': ['Atendente', 'Diretor'],
            'can_manage_paciente_all':  ['Atendente'],
            
            'can_create_atendente': ['Atendente', 'Diretor'],
            'can_manage_atendente_all': ['Diretor'],
            
            'can_create_diretor': ['Diretor'],
            'can_manage_diretor_all': [],
            
            
            'can_view_realname_and_pseudonym': ['Diretor'],
            
            'can_view_only_enableds_selects': ['Paciente'],
            'can_view_all_states_selects': ['Atendente', 'Diretor'],
            'can_manage_selects': ['Atendente', 'Diretor'],
            'can_create_in_any_state': ['Atendente', 'Diretor'],
            'can_create_only_tocheck': ['Paciente'],
            'can_view_selfs': ['Paciente'],
            
            'can_create_solicitacoes_for_any': ['Atendente', 'Diretor'],
            'can_create_solicitacoes_for_self': ['Paciente'],
            
            'can_list_solicitacoes_all': ['Atendente', 'Diretor'],
            'can_list_solicitacoes_self': ['Paciente']
        }
        
        
        
        groups = {
            'Paciente': None,
            'Atendente': None,
            'Diretor': None,
        }
        User_content_type = ContentType.objects.get_for_model(PermissionContentType)
        
        
        for group_name, _ in groups.items():
            
            groups[group_name] = Group.objects.create(name=group_name)
            self.stdout.write(self.style.SUCCESS(f'Grupo "{group_name}" criado com sucesso.'))
            
            role_permission_name = f'role-{group_name}'
            
            permission, created = Permission.objects.get_or_create(
                codename=role_permission_name,
                name=f'Role {group_name}',
                content_type=User_content_type
            )
            self.stdout.write(self.style.SUCCESS(f'Role "{role_permission_name}" adicionada ao grupo "{group_name}".'))
            groups[group_name].permissions.add(permission)
            

        # Criação das permissões e dos grupos com o sufixo "-Permissions"
        for permission_codename, group_names in permissions.items():
            # Criação da permissão
            permission, created = Permission.objects.get_or_create(
                codename=permission_codename,
                name=f'Pode {permission_codename.replace("_", " ")}',
                content_type=User_content_type
            )
            
            # Criação dos grupos e atribuição de permissões
            for group_name in group_names:

                # Adiciona a permissão ao grupo com o sufixo "-Permissions"
                groups[group_name].permissions.add(permission)
                
            self.stdout.write(self.style.SUCCESS(f'Permissão "{permission_codename}" adicionada aos grupos "{group_names}".'))
    

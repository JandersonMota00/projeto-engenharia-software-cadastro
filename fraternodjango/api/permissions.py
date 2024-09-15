from django.http import HttpRequest
from rest_framework import permissions


class CreateUserPermission(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view):
        
        user = request.user
        print(user)
        newUser_user_type = request.data.get('user_type')
        print(newUser_user_type)
        
        # Permitir que usuários não autenticados criem contas de Paciente
        if (newUser_user_type == 'Paciente' and not user.is_authenticated):
            
            return True

        # Restringir Atendentes de criar qualquer tipo de conta
        if (newUser_user_type == 'Atendente' and
            user.is_authenticated and
            user.has_perm('api.can_register_atendente')):

            return True

        # Permitir que Diretores criem contas de Atendentes e Diretores
        if (newUser_user_type == 'Diretor' and 
            user.is_authenticated and 
            user.has_perm('api.can_register_diretor')):
            
            return True

        return False


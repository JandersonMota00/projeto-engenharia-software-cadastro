from django.http import HttpRequest
from rest_framework import permissions


class CreateUserPermission(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view):
        
        user = request.user
        user_type = request.data.get('user_type')
        
        
        # Permitir que usuários não autenticados criem contas de Paciente
        if (user_type == 'PAC' and 
            not request.user.is_authenticated):
            
            return True

        # Restringir Atendentes de criar qualquer tipo de conta
        if (user_type == 'ATD' and
            request.user.is_authenticated and
            request.user.has_perm('api.can_register_atendente')):

            return True

        # Permitir que Diretores criem contas de Atendentes e Diretores
        if (user_type == 'DIR' and 
            request.user.is_authenticated and 
            request.user.has_perm('can_register_diretor')):
            
            return True

        return False


from django.http import HttpRequest
from rest_framework import permissions, views, generics, viewsets
from django.contrib.auth.models import AbstractUser

class CreateUserTypeCheck(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: viewsets.ViewSet):
        
        request_user: AbstractUser = request.user
        
        newUser_user_type = request.data.get('user_type')        
        
        # So deve fazer qualquer verificação se for uma criação
        if view.action != 'create': return True
        
        # TODO Setar permissão create paciente para usuario anonimo
        # if (newUser_user_type == 'Paciente' and request_user.has_perm('can_create_paciente')): return True

        # Permitir que todos usuários criem contas de Paciente
        if (newUser_user_type == 'Paciente'): return True


        if (newUser_user_type == 'Atendente' and request_user.has_perm('can_create_atendente')): return True
        
        
        if (newUser_user_type == 'Diretor' and request_user.has_perm('can_create_diretor')): return True


        return False


class UserPermission(permissions.BasePermission):
    """
    Verifica as permissoes de um usuario sobre um UserModel qualquer
    """
    
    def has_permission(self, request: HttpRequest, view):
        # TODO Django perm
        # FIXME Aplicar permissoes que atendente n pode mexer com diretor
        # Se for atendente
        if request.user.has_perm("role-Atendente"):
            return True
        
        if view.action == 'list':
            print('Voce nao tem permissão para listar os usuarios')
            return False
        
        return self.has_object_permission(request, view, None)



    # Controla permissão sobre um registro no banco de dados, no caso o User do usuario que está chamando a view
    def has_object_permission(self, request: HttpRequest, view, obj):
        """
        Verifica as permissoes de um usuario sobre um UserModel especifico
        """
         
        # Se for uma operação de criação, `obj` será `None`, e qualquer usuario tem permissão para criar
        if not obj:
            return True
        
        
        request_user = request.user
        obj_user: AbstractUser = obj
        
        
        # Se o usuario estiver manipulando sua propia conta
        if request_user.id == obj_user.id and request_user.has_perm('can_manage_user_self'): return True
        
    
        if obj_user.has_perm('role-Atendente') and request_user.has_perm('can_manage_atendente_all'): return True
        
        
        if obj_user.has_perm('role-Diretor') and request_user.has_perm('can_manage_diretor_all'): return True
        
        
        print("Voce não tem permissão sobre esse usuario")
        return False
       
       
class IsStaff(permissions.BasePermission):
    
    def has_permission(self, request: HttpRequest, view):
        # TODO Django perm
        
        # Se for atendente
        if request.user.has_perm("atendente") or request.user.has_perm('diretor'):
            return True
        else:
            return False



class PacientePermissions(permissions.BasePermission):
    
    def has_permission(self, request, view):
        match self.action:
            case 'list':
                return 
            case 'retrieve':
                return 
            case 'create':
                return 
            case 'update':
                return 
            case 'partial_update':
                return 
            case 'destroy':
                return 
            case _:
                return false



class SolitacaoPermissons(permissions.BasePermission):
    
    def has_permission(self, request, view):
        match self.action:
            case 'list':
                return 
            case 'retrieve':
                return 
            case 'create':
                return 
            case 'update':
                return 
            case 'partial_update':
                return 
            case 'destroy':
                return 
            case _:
                return false
    
    
    
    

from rest_framework import viewsets, generics, status, permissions, views, mixins
from django.contrib.auth.models import User
from api import models as apiModels, serializers as apiSerializers, permissions as apiPermissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from .utils import get_user_type
from django.http import HttpRequest
from knox.views import LoginView as KnoxLoginView


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all();
    serializer_class = apiSerializers.UserSerializer
    permission_classes = [apiPermissions.CreateUserTypeCheck, apiPermissions.UserPermission]


# #  View para criação de contas
# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = apiSerializers.RegisterSerializer
#     permission_classes = [apiPermissions.CreateUserTypeCheck]


class LoginView(KnoxLoginView):
    permission_classes = []
    serializer_class = apiSerializers.LoginSerializer  # Adicione o serializer_class

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
# ==================================================================================

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Paciente.objects.all()
    serializer_class = apiSerializers.PacienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Define o paciente logado como o paciente da solicitação
        serializer.save(user=self.request.user)

    
    #     def perform_create(self, serializer):
    #     print('performe create')
    #     serializer.save(user=self.request.user)


# class SelectValueViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = apiSerializers.SelectValueSerializer
    
#     def get_queryset(self):
#         # Verificar a role do usuário e ajustar o queryset
#         if self.request.user.has_perm('can_view_only_enableds_state'):
#             return apiModels.SelectValue.objects.filter(state='ENA')
#         else:
#             return apiModels.SelectValue.objects.all()

# class EnderecoViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = apiModels.Endereco.objects.all()
#     serializer_class = apiSerializers.EnderecoSerializer


# class NumeroDeTelefoneViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = apiModels.NumeroDeTelefone.objects.all()
#     serializer_class = apiSerializers.NumeroDeTelefoneSerializer


# class EmailViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = apiModels.Email.objects.all()
#     serializer_class = apiSerializers.EmailSerializer


class SolicitacaoAtendimentoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = apiSerializers.SolicitacaoAtendimentoSerializer

    def perform_create(self, serializer):
        serializer.save(paciente=apiModels.Paciente.objects.get(user=self.request.user))

    def get_queryset(self):
        user = self.request.user
        
        # Atendentes e diretores podem visualizar todas as solicitações
        if user.has_perm('can_list_solicitacoes_all'):
            return apiModels.SolicitacaoAtendimento.objects.all()
        
        # Pacientes só podem visualizar suas próprias solicitações
        if user.has_perm('can_list_solicitacoes_self'):
            return apiModels.SolicitacaoAtendimento.objects.filter(paciente=user.paciente)
        
        # Se não tiver permissão, retorna uma queryset vazia
        return apiModels.SolicitacaoAtendimento.objects.none()

from rest_framework import viewsets, permissions, mixins
from django.contrib.auth.models import User
from api import models as apiModels, serializers as apiSerializers, permissions as apiPermissions
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView

class LoginView(KnoxLoginView):
    permission_classes = []
    serializer_class = apiSerializers.LoginSerializer  # Adicione o serializer_class

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all();
    serializer_class = apiSerializers.UserSerializer
    permission_classes = [apiPermissions.CreateUserTypeCheck, apiPermissions.UserPermission]




class PacienteViewSet(viewsets.ModelViewSet):
    queryset = apiModels.Paciente.objects.all()
    serializer_class = apiSerializers.PacienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Define o paciente logado como o paciente da solicitação
        # serializer.save(paciente=apiModels.Paciente.objects.get(user=self.request.user))
        serializer.save(user=self.request.user)



class SolicitacaoAtendimentoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = apiSerializers.SolicitacaoAtendimentoSerializer

    def perform_create(self, serializer):
        serializer.save(paciente=apiModels.Paciente.objects.get(user=self.request.user))

    def get_queryset(self):
        user = self.request.user
        
        # Atendentes e diretores podem visualizar todas as solicitações
        if user.has_perm('api.can_list_solicitacoes_all'):
            return apiModels.SolicitacaoAtendimento.objects.all()
        
        print(user.has_perm('api.can_list_solicitacoes_self'))
        
        # Pacientes só podem visualizar suas próprias solicitações
        if user.has_perm('api.can_list_solicitacoes_self'):
            print('has perm')
            print(apiModels.SolicitacaoAtendimento.objects.filter(paciente=apiModels.Paciente.objects.get(user=self.request.user)))
    
            return apiModels.SolicitacaoAtendimento.objects.filter(paciente=apiModels.Paciente.objects.get(user=self.request.user))
        
        # Se não tiver permissão, retorna uma queryset vazia
        return apiModels.SolicitacaoAtendimento.objects.none()

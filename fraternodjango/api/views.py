from rest_framework import viewsets, generics, status, permissions, views, mixins
from django.contrib.auth.models import User
from api import models as apiModels, serializers as apiSerializers, permissions as apiPermissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from .utils import get_user_type

#  View para criação de contas
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = apiSerializers.RegisterSerializer
    permission_classes = [apiPermissions.CreateUserPermission]

class LoginView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = apiSerializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = apiSerializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.id,
            "user_type": get_user_type(user),
        }, status=status.HTTP_200_OK)


def PrimeiroAtendimento():
    pass

class SelectValueViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = apiSerializers.SelectValueSerializer
    
    def get_queryset(self):
        # Verificar a role do usuário e ajustar o queryset
        if self.request.user.has_perm('can_view_only_enableds_state'):
            return apiModels.SelectValue.objects.filter(state='ENA')
        else:
            return apiModels.SelectValue.objects.all()
        
    
class PacienteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = apiModels.Paciente.objects.all()
    serializer_class = apiSerializers.PacienteSerializer


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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = apiSerializers.SolicitacaoAtendimentoSerializer

    def get_queryset(self):
        user = self.request.user
        
        # Atendentes e diretores podem visualizar todas as solicitações
        if user.has_perm('api.can_view_all'):
            return apiModels.SolicitacaoAtendimento.objects.all()
        
        # Pacientes só podem visualizar suas próprias solicitações
        if user.has_perm('api.can_view_only_owns'):
            return apiModels.SolicitacaoAtendimento.objects.filter(paciente=user.paciente)
        
        # Se não tiver permissão, retorna uma queryset vazia
        return apiModels.SolicitacaoAtendimento.objects.none()

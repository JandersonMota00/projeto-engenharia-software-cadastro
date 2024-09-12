from rest_framework import viewsets, generics, status, permissions, views
from django.contrib.auth.models import User
from api import models as apiModels, serializers as apiSerializers, permissions as apiPermissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response


#  View para criação de contas
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = apiSerializers.RegisterSerializer
    permission_classes = [apiPermissions.CreateUserPermission]


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
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
            "user_type": user.user_type,
        }, status=status.HTTP_200_OK)

class SelectValueViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = apiModels.SelectValue.objects.all()
    serializer_class = apiSerializers.SelectValueSerializer
    
    
class PacienteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = apiModels.Paciente.objects.all()
    serializer_class = apiSerializers.PacienteSerializer


class EnderecoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = apiModels.Endereco.objects.all()
    serializer_class = apiSerializers.EnderecoSerializer


class NumeroDeTelefoneViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = apiModels.NumeroDeTelefone.objects.all()
    serializer_class = apiSerializers.NumeroDeTelefoneSerializer


class EmailViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = apiModels.Email.objects.all()
    serializer_class = apiSerializers.EmailSerializer


class SolicitacaoAtendimentoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = apiModels.SolicitacaoAtendimento.objects.all()
    serializer_class = apiSerializers.SolicitacaoAtendimentoSerializer

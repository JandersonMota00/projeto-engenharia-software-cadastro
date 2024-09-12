from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SelectValueViewSet, PacienteViewSet, EnderecoViewSet,
    NumeroDeTelefoneViewSet, EmailViewSet, SolicitacaoAtendimentoViewSet, RegisterView, LoginView
)

# Criando um roteador padrão
router = DefaultRouter()
router.register(r'select-values', SelectValueViewSet)
router.register(r'pacientes', PacienteViewSet)
router.register(r'enderecos', EnderecoViewSet)
router.register(r'numeros-telefone', NumeroDeTelefoneViewSet)
router.register(r'emails', EmailViewSet)
router.register(r'solicitacoes-atendimento', SolicitacaoAtendimentoViewSet)


# Incluindo as rotas no urlpatterns
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]

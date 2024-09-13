from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
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

# urlpatterns = [
#     # YOUR PATTERNS
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     # Optional UI:
#     path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
# ]



# Incluindo as rotas no urlpatterns
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]

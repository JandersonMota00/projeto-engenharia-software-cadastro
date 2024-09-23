from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SolicitacaoAtendimentoViewSet, LoginView, PacienteViewSet, UserView
    # EnderecoViewSet, NumeroDeTelefoneViewSet, EmailViewSet
)
from knox import views as knox_views

# Criando um roteador padrão
router = DefaultRouter()
# router.register(r'select-values', 'select-values')
router.register(r'users', UserView, basename='users')
router.register(r'pacientes', PacienteViewSet, 'pacientes')
router.register(r'solicitacoes', SolicitacaoAtendimentoViewSet, 'solicitacoes')

# router.register(r'select-values/(?P<selecttype>[^/]+)', SelectValueViewSet, basename='select-value')
# router.register(r'enderecos', EnderecoViewSet)
# router.register(r'numeros-telefone', NumeroDeTelefoneViewSet)
# router.register(r'emails', EmailViewSet)

# urlpatterns = [
#     # YOUR PATTERNS
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     # Optional UI:
#     path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
# ]



# Incluindo as rotas no urlpatterns
urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]


urlpatterns += [
     path(r'auth/login/', LoginView.as_view(), name='knox_login'),
     path(r'auth/logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
     path(r'auth/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]


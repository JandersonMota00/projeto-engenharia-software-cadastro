from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    ReligiaoValueViewSet, GeneroValueViewSet, OrientacaoSexualValueViewSet,
    TratamentoValueViewSet, SintomaValueViewSet, DoencaValueViewSet,
    AlergiaValueViewSet, MedicamentoValueViewSet
)

# Crie o roteador e registre as rotas
router = DefaultRouter()
router.register(r'religiao', ReligiaoValueViewSet, basename='religiao')
router.register(r'genero', GeneroValueViewSet, basename='genero')
router.register(r'orientacao', OrientacaoSexualValueViewSet, basename='orientacao')
router.register(r'tratamento', TratamentoValueViewSet, basename='tratamento')
router.register(r'sintoma', SintomaValueViewSet, basename='sintoma')
router.register(r'doenca', DoencaValueViewSet, basename='doenca')
router.register(r'alergia', AlergiaValueViewSet, basename='alergia')
router.register(r'medicamento', MedicamentoValueViewSet, basename='medicamento')

urlpatterns = [
    path('', include(router.urls)),
]

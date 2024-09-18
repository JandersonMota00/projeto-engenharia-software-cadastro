from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    ReligiaoValue, GeneroValue, OrientacaoSexualValue, TratamentoValue,
    SintomaValue, DoencaValue, AlergiaValue, MedicamentoValue, BaseSelectValue
)
from .serializers import (
    ReligiaoValueSerializer, GeneroValueSerializer, OrientacaoSexualValueSerializer,
    TratamentoValueSerializer, SintomaValueSerializer, DoencaValueSerializer,
    AlergiaValueSerializer, MedicamentoValueSerializer
)

from django.db.models import Model

class BaseSelectValueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtra os objetos com base no estado ou outras condições.
        """
        
        queryset = self.get_model_class().objects.all()
        
        if self.action == 'list':
            
            search_term = self.request.query_params.get('search', '')
            
            print(search_term)
            
            normalized_search_term = self.model_class.normalize(search_term)
            
            queryset = queryset.filter(normalized_value__icontains=normalized_search_term, state='ENA')[:10]
            
            
            
        if self.request.user.has_perm('role-Paciente'):
            
            queryset = queryset.filter(state='ENA')
        
            

        return queryset

        
    def get_model_class(self) -> Model:
        
        return self.model_class
        
        

    def get_serializer_class(self) -> serializers.ModelSerializer:
        """
        Retorna o serializer correto com base no ViewSet.
        """
        return self.serializer_class


class ReligiaoValueViewSet(BaseSelectValueViewSet):
    model_class = ReligiaoValue
    serializer_class = ReligiaoValueSerializer


class GeneroValueViewSet(BaseSelectValueViewSet):
    model_class = GeneroValue
    serializer_class = GeneroValueSerializer


class OrientacaoSexualValueViewSet(BaseSelectValueViewSet):
    model_class = OrientacaoSexualValue
    serializer_class = OrientacaoSexualValueSerializer


class TratamentoValueViewSet(BaseSelectValueViewSet):
    model_class = TratamentoValue
    serializer_class = TratamentoValueSerializer


class SintomaValueViewSet(BaseSelectValueViewSet):
    model_class = SintomaValue
    serializer_class = SintomaValueSerializer


class DoencaValueViewSet(BaseSelectValueViewSet):
    model_class = DoencaValue
    serializer_class = DoencaValueSerializer


class AlergiaValueViewSet(BaseSelectValueViewSet):
    model_class = AlergiaValue
    serializer_class = AlergiaValueSerializer


class MedicamentoValueViewSet(BaseSelectValueViewSet):
    model_class = MedicamentoValue
    serializer_class = MedicamentoValueSerializer

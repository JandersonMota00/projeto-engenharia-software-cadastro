from rest_framework import serializers
from .models import (
    ReligiaoValue, GeneroValue, OrientacaoSexualValue, TratamentoValue,
    SintomaValue, DoencaValue, AlergiaValue, MedicamentoValue
)

from rest_framework import serializers

class BaseValueSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

class ReligiaoValueSerializer(BaseValueSerializer):
    class Meta(BaseValueSerializer.Meta):
        model = ReligiaoValue

class GeneroValueSerializer(BaseValueSerializer):
    class Meta(BaseValueSerializer.Meta):
        model = GeneroValue

class OrientacaoSexualValueSerializer(BaseValueSerializer):
    class Meta(BaseValueSerializer.Meta):
        model = OrientacaoSexualValue

class TratamentoValueSerializer(BaseValueSerializer):
    class Meta(BaseValueSerializer.Meta):
        model = TratamentoValue

class SintomaValueSerializer(BaseValueSerializer):
    class Meta(BaseValueSerializer.Meta):
        model = SintomaValue

class DoencaValueSerializer(BaseValueSerializer):
    class Meta(BaseValueSerializer.Meta):
        model = DoencaValue

class AlergiaValueSerializer(BaseValueSerializer):
    class Meta(BaseValueSerializer.Meta):
        model = AlergiaValue

class MedicamentoValueSerializer(BaseValueSerializer):
    class Meta(BaseValueSerializer.Meta):
        model = MedicamentoValue

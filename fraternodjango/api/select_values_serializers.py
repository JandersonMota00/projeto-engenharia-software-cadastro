from rest_framework import serializers
from .models import (
    ReligiaoValue, GeneroValue, OrientacaoSexualValue, TratamentoValue,
    SintomaValue, DoencaValue, AlergiaValue, MedicamentoValue
)

class ReligiaoValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReligiaoValue
        fields = '__all__'

class GeneroValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneroValue
        fields = '__all__'

class OrientacaoSexualValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrientacaoSexualValue
        fields = '__all__'

class TratamentoValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TratamentoValue
        fields = '__all__'

class SintomaValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SintomaValue
        fields = '__all__'

class DoencaValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoencaValue
        fields = '__all__'

class AlergiaValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlergiaValue
        fields = '__all__'

class MedicamentoValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicamentoValue
        fields = '__all__'
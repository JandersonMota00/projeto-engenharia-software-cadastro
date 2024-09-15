from rest_framework import serializers, validators
from api import models as apiModels
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .utils import get_user_type

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    
    username = serializers.CharField(
        required=True,
        min_length=8,
        max_length=32,
    )
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )

    user_type = serializers.ChoiceField(
        write_only=True,
        required=True, 
        choices=['Paciente', 'Atendente', 'Diretor'],
    )
    

    
    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        
        # Adicionando o usuário ao grupo apropriado
        if validated_data["user_type"] == 'Paciente':
            group = Group.objects.get(name='Paciente')
            
        elif validated_data["user_type"] == 'Atendente':
            group = Group.objects.get(name='Atendente')
            
        elif validated_data["user_type"] == 'Diretor':
            group = Group.objects.get(name='Diretor')
            
        else:
            group = None
        
        if group:
            user.groups.add(group)
        
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_type'] = get_user_type(instance)
        return representation

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Credenciais inválidas.")
        else:
            raise serializers.ValidationError("Por favor, insira o nome de usuário e a senha.")
        
        attrs['user'] = user
        return attrs
    
    
# ==================================================================================

class SelectValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.SelectValue
        fields = ['id', 'select_type', 'value', 'normalized_value', 'state']
    
    
class PacienteSerializer(serializers.ModelSerializer):
    genero = SelectValueSerializer(many=True)
    orientacao_sexual = SelectValueSerializer(many=True)
    religiao = SelectValueSerializer(many=True)
    alergias = SelectValueSerializer(many=True)

    class Meta:
        model = apiModels.Paciente
        fields = [
            'id', 'nome', 'pseudonimo', 'data_nascimento', 
            'genero', 'orientacao_sexual', 'religiao', 'alergias', 
            'ja_fez_psicoterapia', 'ja_fez_psiquiatrico', 'ja_fez_tratamento_espirita'
        ]
        

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.Endereco
        fields = ['id', 'paciente', 'cep', 'estado', 'cidade', 'bairro', 
                  'tipo_logradouro', 'logradouro', 'numero', 'complemento']

class NumeroDeTelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.NumeroDeTelefone
        fields = ['id', 'paciente', 'rotulo', 'ddd', 'telefone', 
                  'whatsapp', 'telegram', 'ligacao']

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.Email
        fields = ['id', 'paciente', 'email']

class SolicitacaoAtendimentoSerializer(serializers.ModelSerializer):
    sintomas = SelectValueSerializer(many=True)
    tratamentos_em_andamento = SelectValueSerializer(many=True)

    class Meta:
        model = apiModels.SolicitacaoAtendimento
        fields = ['id', 'descricao', 'sintomas', 'tratamentos_em_andamento']



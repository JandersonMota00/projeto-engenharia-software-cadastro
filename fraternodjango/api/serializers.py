from rest_framework import serializers, validators
from api import models as apiModels
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from . import models

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'id']
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save();

        user_type = self.context.get('user_type', 'Paciente')

        # Adicionando o usuário ao grupo apropriado
        if user_type == 'Paciente':
            group = Group.objects.get(name='Paciente')

        elif user_type == 'Atendente':
            group = Group.objects.get(name='Atendente')

        elif user_type == 'Diretor':
            group = Group.objects.get(name='Diretor')

        else:
            group = None

        if group:
            user.groups.add(group)

        return user


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
            raise serializers.ValidationError(
                "Por favor, insira o nome de usuário e a senha.")

        attrs['user'] = user
        attrs['id'] = user.id
        return attrs

# ==================================================================================


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.Endereco
        fields = ['cep', 'estado', 'cidade', 'bairro',
                  'tipo_logradouro', 'logradouro', 'numero', 'complemento']

    def create_or_update_endereco(self, validated_data):
        # Verifica se o paciente já tem um endereço
        paciente = self.context['patient']
        endereco, created = apiModels.Endereco.objects.update_or_create(
            paciente=paciente,
            defaults=validated_data
        )
        return endereco


class NumeroDeTelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.NumeroDeTelefone
        fields = ['rotulo', 'ddd', 'telefone',
                  'whatsapp', 'telegram', 'ligacao']

    def create_or_update_telefone(self, validated_data):
        paciente = self.context['patient']
        telefone, created = apiModels.NumeroDeTelefone.objects.update_or_create(
            paciente=paciente,
            rotulo=validated_data['rotulo'],
            defaults=validated_data
        )
        return telefone


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.Email
        fields = ['email']

    def create_or_update_email(self, validated_data):
        
        paciente = self.context['patient']
        
        email, created = apiModels.Email.objects.update_or_create(
            paciente=paciente,
            email=validated_data['email'],
            defaults=validated_data
        )
        return email



class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.Paciente
        exclude = ['user']
        






class SolicitacaoAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.SolicitacaoAtendimento
        exclude = ['paciente']


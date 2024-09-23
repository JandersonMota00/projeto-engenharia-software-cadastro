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
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

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


class NumeroDeTelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.NumeroDeTelefone
        fields = ['ddd', 'telefone', 'whatsapp', 'telegram', 'ligacao']


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.Endereco
        fields = ['cep', 'estado', 'cidade', 'bairro',
                  'logradouro', 'numero', 'complemento']


class PacienteSerializer(serializers.ModelSerializer):    
    endereco = EnderecoSerializer()  # Nested field for endereco

    # Nested field for telefone principal
    telefone_principal = NumeroDeTelefoneSerializer()
    telefone_secundario = NumeroDeTelefoneSerializer(
        required=False)  # Nested field for telefone secundario

    class Meta:
        model = apiModels.Paciente
        fields = [
            'nome', 'nome_social', 'pseudonimo', 'data_nascimento',
            'sexo', 'genero', 'religiao', 'alergias', 'ja_fez_psicoterapia',
            'ja_fez_psiquiatrico', 'ja_fez_tratamento_espirita',
            'endereco', 'telefone_principal', 'telefone_secundario'
        ]

    def create(self, validated_data):
        
        # Extraindo dados dos relacionamentos aninhados]
        endereco_data = validated_data.pop('endereco', None)

        telefone_principal_data = validated_data.pop(
            'telefone_principal', None)
        telefone_secundario_data = validated_data.pop(
            'telefone_secundario', None)

        alergias_data = validated_data.pop('alergias', None)

        # Criação de instâncias relacionadas se os dados estiverem presentes

        endereco = apiModels.Endereco.objects.create(**endereco_data)
        telefone_principal = apiModels.NumeroDeTelefone.objects.create(
            **telefone_principal_data)

        if telefone_secundario_data:
            telefone_secundario = apiModels.NumeroDeTelefone.objects.create(
                **telefone_secundario_data)
        else:
            telefone_secundario = None

        # Criação do paciente com os campos opcionais
        paciente_data = {**validated_data,
                         'endereco': endereco,
                         'telefone_principal': telefone_principal}  # Inicia com os dados validados

        if telefone_secundario:
            # Adiciona o telefone secundário se existe
            paciente_data['telefone_secundario'] = telefone_secundario

        paciente = apiModels.Paciente.objects.create(**paciente_data)

        if alergias_data:
            paciente.alergias.set(alergias_data)  # Adicionando as alergias

        return paciente

    def update(self, instance, validated_data):
        endereco_data = validated_data.pop('endereco', None)

        telefone_principal_data = validated_data.pop(
            'telefone_principal', None)
        telefone_secundario_data = validated_data.pop(
            'telefone_secundario', None)

        alergias_data = validated_data.pop('alergias', None)

        apiModels.Endereco.objects.filter(
            id=instance.endereco.id).update(**endereco_data)

        apiModels.NumeroDeTelefone.objects.filter(
            id=instance.telefone_principal.id).update(**telefone_principal_data)

        
        if telefone_secundario_data:
            apiModels.NumeroDeTelefone.objects.filter(
                id=instance.telefone_secundario.id).update(**telefone_secundario_data)

        # Atualizando o próprio paciente
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Usar o método set() para o campo ManyToMany
        instance.alergias.set(alergias_data)

        instance.save()
        return instance


class SolicitacaoAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.SolicitacaoAtendimento
        exclude = ['paciente']

from rest_framework import serializers, validators
from api import models as apiModels
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .utils import get_user_type

from .select_values_serializers import *

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        write_only_fields = ['password']
    
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

# class RegisterSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[validators.UniqueValidator(queryset=User.objects.all())]
#     )

#     username = serializers.CharField(
#         validators=[validators.UniqueValidator(queryset=User.objects.all())],
#         required=True,
#         min_length=8,
#         max_length=32,
#     )

#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         validators=[validate_password]
#     )

#     user_type = serializers.ChoiceField(
#         write_only=True,
#         required=True,
#         choices=['Paciente', 'Atendente', 'Diretor'],
#     )

#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email']
#         )
#         user.set_password(validated_data['password'])
#         user.save();

#         # Adicionando o usuário ao grupo apropriado
#         if validated_data["user_type"] == 'Paciente':
#             group = Group.objects.get(name='Paciente')

#         elif validated_data["user_type"] == 'Atendente':
#             group = Group.objects.get(name='Atendente')

#         elif validated_data["user_type"] == 'Diretor':
#             group = Group.objects.get(name='Diretor')

#         else:
#             group = None

#         if group:
#             user.groups.add(group)

#         return user

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['user_type'] = get_user_type(instance)
#         return representation

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
    generos = GeneroValueSerializer(many=True, write_only=True)
    orientacoes_sexuais = OrientacaoSexualValueSerializer(many=True, write_only=True)
    religioes = ReligiaoValueSerializer(many=True, write_only=True)
    alergias = AlergiaValueSerializer(many=True, write_only=True)

    endereco = EnderecoSerializer(write_only=True, required=False)
    emails = EmailSerializer(many=True, write_only=True, required=False)
    telefones = NumeroDeTelefoneSerializer(many=True, write_only=True, required=False)

    read_only_fields = ['id']

    class Meta:
        model = apiModels.Paciente
        fields = ['id', 'nome', 'pseudonimo', 'data_nascimento', 'generos', 'emails',
                  'orientacoes_sexuais', 'religioes', 'alergias', 'endereco', 'telefones',
                  'ja_fez_psicoterapia', 'ja_fez_psiquiatrico', 'ja_fez_tratamento_espirita',
                  'user_id']

    def create(self, validated_data):
        generos_data = validated_data.pop('generos', [])
        orientacoes_data = validated_data.pop('orientacoes_sexuais', [])
        religioes_data = validated_data.pop('religioes', [])
        alergias_data = validated_data.pop('alergias', [])
        endereco_data = validated_data.pop('endereco', None)
        emails_data = validated_data.pop('emails', [])
        telefones_data = validated_data.pop('telefones', [])
        user_id = validated_data.pop('user_id', None)

        # Use o ID do usuário logado se `user_id` não for fornecido
        user = self.context['request'].user if user_id is None else User.objects.get(id=user_id)

        paciente = apiModels.Paciente.objects.create(user=user, **validated_data)

        self._handle_values(paciente, generos_data,
                            'genero', GeneroValueSerializer)
        self._handle_values(paciente, orientacoes_data,
                            'orientacao_sexual', OrientacaoSexualValueSerializer)
        self._handle_values(paciente, religioes_data,
                            'religiao', ReligiaoValueSerializer)
        self._handle_values(paciente, alergias_data,
                            'alergias', AlergiaValueSerializer)

        if endereco_data:
            endereco_serializer = EnderecoSerializer(
                data=endereco_data, context={'patient': paciente})
            endereco_serializer.is_valid(raise_exception=True)
            endereco_serializer.create_or_update_endereco(
                endereco_serializer.validated_data)

        for email_data in emails_data:
            email_serializer = EmailSerializer(
                data=email_data, context={'patient': paciente})
            email_serializer.is_valid(raise_exception=True)
            email_serializer.create_or_update_email(
                email_serializer.validated_data)

        for telefone_data in telefones_data:
            telefone_serializer = NumeroDeTelefoneSerializer(
                data=telefone_data, context={'patient': paciente})
            telefone_serializer.is_valid(raise_exception=True)
            telefone_serializer.create_or_update_telefone(
                telefone_serializer.validated_data)

        return paciente

    def update(self, instance, validated_data):
        generos_data = validated_data.pop('generos', [])
        orientacoes_data = validated_data.pop('orientacoes_sexuais', [])
        religioes_data = validated_data.pop('religioes', [])
        alergias_data = validated_data.pop('alergias', [])
        endereco_data = validated_data.pop('endereco', None)
        emails_data = validated_data.pop('emails', [])
        telefones_data = validated_data.pop('telefones', [])
        user_id = validated_data.pop('user_id', None)

        # Use o ID do usuário logado se `user_id` não for fornecido
        user = self.context['request'].user if user_id is None else User.objects.get(id=user_id)

        # Atualiza o paciente, mantendo o `id` original
        instance = super().update(instance, validated_data)
        instance.user = user
        instance.save()

        self._handle_values(instance, generos_data,
                            'genero', GeneroValueSerializer)
        self._handle_values(instance, orientacoes_data,
                            'orientacao_sexual', OrientacaoSexualValueSerializer)
        self._handle_values(instance, religioes_data,
                            'religiao', ReligiaoValueSerializer)
        self._handle_values(instance, alergias_data,
                            'alergias', AlergiaValueSerializer)

        if endereco_data:
            endereco_serializer = EnderecoSerializer(
                instance.endereco, data=endereco_data, context={'patient': instance})
            endereco_serializer.is_valid(raise_exception=True)
            endereco_serializer.create_or_update_endereco(
                endereco_serializer.validated_data)

        for email_data in emails_data:
            email_serializer = EmailSerializer(
                data=email_data, context={'patient': instance})
            email_serializer.is_valid(raise_exception=True)
            email_serializer.create_or_update_email(
                email_serializer.validated_data)

        for telefone_data in telefones_data:
            telefone_serializer = NumeroDeTelefoneSerializer(
                data=telefone_data, context={'patient': instance})
            telefone_serializer.is_valid(raise_exception=True)
            telefone_serializer.create_or_update_telefone(
                telefone_serializer.validated_data)

        return instance

    def _handle_values(self, instance, values_data, field_name, serializer_class):
        values = []
        for value_data in values_data:
            serializer = serializer_class(data=value_data)
            serializer.is_valid(raise_exception=True)
            value_instance = serializer.create_or_update_value(
                serializer.validated_data)
            values.append(value_instance)

        # Atribui os valores à relação ManyToMany do paciente
        getattr(instance, field_name).set(values)





class SolicitacaoAtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = apiModels.SolicitacaoAtendimento
        fields = '__all__'

    def validate(self, attrs):
        # Verifica se o paciente na solicitação é o próprio usuário autenticado
        user = self.context['request'].user

        if hasattr(user, 'paciente') and attrs.get('paciente') != user.paciente:
            raise serializers.ValidationError(
                "Você só pode criar solicitações para você mesmo.")

        return attrs

    def create(self, validated_data):
        # Garante que o paciente seja sempre o próprio usuário autenticado
        user = self.context['request'].user
        validated_data['paciente'] = user.paciente
        return super().create(validated_data)


from django.contrib.auth.models import User
import unicodedata
from django.db import models
from django.core.validators import MinLengthValidator
import uuid

# religiao
# genero
# orientacao
# tratamento
# sintoma
# doenca
# alergia
# medicamento


# class SelectValue(models.Model):

#     _SELECT_TYPE_CHOICES = [
#         ('RELIG', 'Religião'),
#         ('GENER', 'Gênero'),
#         ('ORIEN', 'Orientação Sexual'),
#         ('TRATA', 'Tratamento'),
#         ('SINTO', 'Sintoma'),
#         ('DOENC', 'Doença'),
#         ('ALERG', 'Alergia'),
#         ('MEDIC', 'Medicamento'),
#     ]
#     _STATE_CHOICES = [
#         ('ENA', 'enable'),
#         ('DIS', 'disable'),
#         ('TCK', 'tocheck')
#     ]

#     # Select type armazena de qual select é um registro
#     # Por exemplo, um registro para alergia leite seria:
#     # select_type = 'ALERG'
#     # value = 'Leite'

#     select_type = models.CharField(max_length=5, choices=_SELECT_TYPE_CHOICES)
#     value = models.CharField(max_length=256)
#     normalized_value = models.CharField(max_length=256, editable=False)

#     state = models.CharField(choices=_STATE_CHOICES,
#                              max_length=3, default='TCK')

#     class Meta:
#         permissions = [
#             ('can_create_with_any_state', 'Pode criar values com qualquer state'),
#             ('can_create_only_with_tocheck_state', 'Pode criar somente values tocheck'),
#             ('can_view_only_enableds_state', 'Pode visualizar apenas os valores validados'),
#             ('can_view_all_states', 'Pode visualizar values com qualquer valor de state')
#         ]


#     def __str__(self) -> str:
#         return self.state + " # " + self.select_type + " ### " + self.value + ' # ' + str(self.id)

#     def save(self, *args, **kwargs):
#         if self.value:
#             self.normalized_value = SelectValue.normalize(self.value)
#         super().save(*args, **kwargs)

#     @staticmethod
#     def normalize(value: str) -> str:
#         value = value.lower()
#         value = unicodedata.normalize('NFKD', value).encode(
#             'ASCII', 'ignore').decode('ASCII')
#         return value

class BaseSelectValue(models.Model):
    value = models.CharField(max_length=256)
    normalized_value = models.CharField(max_length=256, editable=False)
    state = models.CharField(choices=[
        ('enable', 'enable'),
        ('disable', 'disable'),
        ('tocheck', 'tocheck')
    ], max_length=8, default='tocheck')

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.state} ### {self.value} # {self.id}"

    def save(self, *args, **kwargs):
        if self.value:
            self.normalized_value = self.normalize(self.value)
        super().save(*args, **kwargs)

    @staticmethod
    def normalize(value: str) -> str:
        value = value.lower()
        value = unicodedata.normalize('NFKD', value).encode(
            'ASCII', 'ignore').decode('ASCII')
        return value

# Modelos especializados para cada tipo de SelectValue

class ReligiaoValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Religião'
        verbose_name_plural = 'Religiões'

class GeneroValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'

class OrientacaoSexualValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Orientação Sexual'
        verbose_name_plural = 'Orientações Sexuais'

class TratamentoValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Tratamento'
        verbose_name_plural = 'Tratamentos'

class SintomaValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Sintoma'
        verbose_name_plural = 'Sintomas'

class DoencaValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Doença'
        verbose_name_plural = 'Doenças'

class AlergiaValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Alergia'
        verbose_name_plural = 'Alergias'

class MedicamentoValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'





# Modelo Paciente atualizado
class Paciente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=128)
    pseudonimo = models.CharField(max_length=128)
    data_nascimento = models.DateField()

    # Relacionando com os novos modelos específicos
    genero = models.ManyToManyField(GeneroValue, blank=True, related_name='pacientes')
    orientacao_sexual = models.ManyToManyField(OrientacaoSexualValue, blank=True, related_name='pacientes')
    religiao = models.ManyToManyField(ReligiaoValue, blank=True, related_name='pacientes')
    alergias = models.ManyToManyField(AlergiaValue, blank=True, related_name='pacientes')

    ja_fez_psicoterapia = models.BooleanField()
    ja_fez_psiquiatrico = models.BooleanField()
    ja_fez_tratamento_espirita = models.BooleanField()

    class Meta:
        permissions = [
            ('can_view_realname_and_pseudonym', 'Permite ver nome real e pseudônimo'),
            ('can_view_only_pseudonym', 'Permite ver apenas o pseudonimo'),
        ]

    def __str__(self) -> str:
        return self.nome

class Endereco(models.Model):

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    cep = models.CharField(max_length=8, validators=[MinLengthValidator(8)])

    estado = models.CharField(max_length=100)

    cidade = models.CharField(max_length=64)

    bairro = models.CharField(max_length=100)

    TIPOS_LOGRADOURO = [
        ('NDA', 'Não se aplica'),
        ('OUT', 'Outro'),
        ('RUA', 'Rua'),
        ('AV', 'Avenida'),
        ('TRA', 'Travessa'),
        ('ROD', 'Rodovia'),
        ('AL', 'Alameda'),
        ('PRA', 'Praça'),
        ('EST', 'Estrada'),
        ('VL', 'Vila'),
        ('LRG', 'Largo'),
        ('BC', 'Beco'),
        ('QD', 'Quadra'),
        ('CON', 'Condomínio'),
        ('ST', 'Sítio'),
        ('FZ', 'Fazenda'),
        ('LT', 'Loteamento'),
        ('VL', 'Viela'),
        ('PQ', 'Parque'),
    ]

    tipo_logradouro = models.CharField(
        max_length=4, choices=TIPOS_LOGRADOURO, default='NDA')

    logradouro = models.CharField(max_length=100)

    numero = models.CharField(max_length=5)

    complemento = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return self.cidade + self.bairro

class NumeroDeTelefone(models.Model):

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    rotulo = models.CharField(max_length=16)

    ddd = models.CharField(max_length=15)
    telefone = models.CharField(max_length=16)

    whatsapp = models.BooleanField(default=False, blank=True)
    telegram = models.BooleanField(default=False, blank=True)
    ligacao = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return self.paciente.__str__() + '#'+self.ddd+self.telefone

class Email(models.Model):

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    email = models.CharField(max_length=256)

# Modelo SolicitacaoAtendimento atualizado
class SolicitacaoAtendimento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    descricao = models.TextField()

    # Relacionando com SintomaValue e TratamentoValue
    sintomas = models.ManyToManyField(SintomaValue, blank=True, related_name='solicitacoes')
    tratamentos_em_andamento = models.ManyToManyField(TratamentoValue, blank=True, related_name='solicitacoes')

    class Meta:
        permissions = [
            ('can_view_all', 'Pode ver todas as solicitações de atendimento'),
            ('can_view_only_owns', 'Pode ver apenas suas próprias solicitações de atendimento')
        ]

    def __str__(self) -> str:
        return f"Solicitação de {self.paciente.nome} - {self.id}"

    # TODO transformar o bloco abaixo em sintomas tambem?
    # desmaio = models.BooleanField()
    # vulto = models.BooleanField()
    # vozes = models.BooleanField()
    # pensamentos_suicidas = models.BooleanField()
    # desencarne_ultimo_ano = models.BooleanField()

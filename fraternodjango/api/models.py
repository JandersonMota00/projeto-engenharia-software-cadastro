from django.contrib.auth.models import User
import unicodedata
from django.db import models
from django.core.validators import MinLengthValidator
import uuid
from selectvalues import models as selectModels

class Paciente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=128)
    pseudonimo = models.CharField(max_length=128)
    data_nascimento = models.DateField()

    # Relacionando com os novos modelos específicos
    # genero = models.ManyToManyField(selectModels.GeneroValue, blank=True, related_name='pacientes')
    # orientacao_sexual = models.ManyToManyField(selectModels.OrientacaoSexualValue, blank=True, related_name='pacientes')
    # religiao = models.ManyToManyField(selectModels.ReligiaoValue, blank=True, related_name='pacientes')
    
    genero = models.ForeignKey(selectModels.GeneroValue, on_delete=models.PROTECT, null=True)
    orientacao_sexual = models.ForeignKey(selectModels.OrientacaoSexualValue, on_delete=models.PROTECT, null=True)
    religiao = models.ForeignKey(selectModels.ReligiaoValue, on_delete=models.PROTECT, null=True)

    alergias = models.ManyToManyField(selectModels.AlergiaValue, blank=True, related_name='pacientes')
    
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
    sintomas = models.ManyToManyField(selectModels.SintomaValue, blank=True, related_name='solicitacoes')
    tratamentos_em_andamento = models.ManyToManyField(selectModels.TratamentoValue, blank=True, related_name='solicitacoes')

    

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

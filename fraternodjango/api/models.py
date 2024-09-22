from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator
from selectvalues import models as selectModels


class NumeroDeTelefone(models.Model):

    ddd = models.CharField(max_length=2)
    telefone = models.CharField(max_length=16)

    whatsapp = models.BooleanField(default=False, blank=True)
    telegram = models.BooleanField(default=False, blank=True)
    ligacao = models.BooleanField(default=False, blank=True)


class Endereco(models.Model):

    cep = models.CharField(max_length=8, validators=[MinLengthValidator(8)])

    estado = models.CharField(max_length=128)

    cidade = models.CharField(max_length=64)

    bairro = models.CharField(max_length=128)

    logradouro = models.CharField(max_length=128, blank=True)

    numero = models.CharField(max_length=5, blank=True)

    complemento = models.CharField(max_length=256, blank=True)

    def __str__(self) -> str:
        return self.cidade + self.bairro


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    nome = models.CharField(max_length=128)
    nome_social = models.CharField(max_length=128, blank=True)
    pseudonimo = models.CharField(max_length=128, blank=True)

    data_nascimento = models.DateField()

    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE)

    email = models.EmailField()
    telefone_principal = models.OneToOneField(NumeroDeTelefone,
                                              on_delete=models.CASCADE,
                                              related_name='none+')
    telefone_secundario = models.OneToOneField(NumeroDeTelefone,
                                               on_delete=models.CASCADE,
                                               related_name='none+', null=True, blank=True)

    SEXO_CHOICES = [
        ('MASCULINO', 'Masculino'),
        ('FEMININO', 'Feminino'),
        ('INTERSEXUAL', 'Intersexual'),
        ('NAO_INFORMAR', 'Prefiro não informar'),
    ]

    sexo = models.CharField(choices=SEXO_CHOICES, max_length=15)

    genero = models.ForeignKey(
        selectModels.GeneroValue, on_delete=models.PROTECT, null=True, blank=True)

    religiao = models.ForeignKey(
        selectModels.ReligiaoValue, on_delete=models.PROTECT, null=True, blank=True)

    alergias = models.ManyToManyField(selectModels.AlergiaValue, blank=True)

    ja_fez_psicoterapia = models.BooleanField()
    ja_fez_psiquiatrico = models.BooleanField()
    ja_fez_tratamento_espirita = models.BooleanField()

    class Meta:
        permissions = [
            ('can_view_realname_and_pseudonym',
             'Permite ver nome real e pseudônimo'),
            ('can_view_only_pseudonym', 'Permite ver apenas o pseudonimo'),
        ]

    def __str__(self) -> str:
        return self.nome


class SolicitacaoAtendimento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    
    motivo = models.TextField(blank=True, null=True)

    # Relacionando com SintomaValue e TratamentoValue
    sintomas = models.ManyToManyField(
        selectModels.SintomaValue, blank=True, related_name='solicitacoes')
    tratamentos_em_andamento = models.ManyToManyField(
        selectModels.TratamentoValue, blank=True, related_name='solicitacoes')

    class Meta:
        permissions = [
            ('list_all', 'Pode listar todas as solicitações'),
            ('list_self', 'Pode listar suas propias solicitações'),
            
            ]

    def __str__(self) -> str:
        return f"Solicitação de {self.paciente.nome} - {self.id}"

    # TODO transformar o bloco abaixo em sintomas tambem?
    # desmaio = models.BooleanField()
    # vulto = models.BooleanField()
    # vozes = models.BooleanField()
    # pensamentos_suicidas = models.BooleanField()
    # desencarne_ultimo_ano = models.BooleanField()


class PermissionContentType(models.Model):
    keep = models.BooleanField(null=True)

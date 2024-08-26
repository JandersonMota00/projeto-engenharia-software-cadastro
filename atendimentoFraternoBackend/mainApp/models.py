import unicodedata
from django.db import models
from django.core.validators import MinLengthValidator

# religiao
# genero
# orientacao
# tratamento
# sintoma
# doenca
# alergia
# medicamento


class SelectValue(models.Model):

    _SELECT_TYPE_CHOICES = [
        ('RELIG', 'Religião'),
        ('GENER', 'Gênero'),
        ('ORIEN', 'Orientação Sexual'),
        ('TRATA', 'Tratamento'),
        ('SINTO', 'Sintoma'),
        ('DOENC', 'Doença'),
        ('ALERG', 'Alergia'),
        ('MEDIC', 'Medicamento'),
    ]

    # Select type armazena de qual select é um registro
    # Por exemplo, um registro para alergia leite seria:
    # select_type = 'ALERG'
    # value = 'Leite'

    select_type = models.CharField(max_length=5, choices=_SELECT_TYPE_CHOICES)
    value = models.CharField(max_length=256)
    normalized_value = models.CharField(max_length=256, editable=False)

    _STATE_CHOICES = [
        ('ENA', 'enable'),
        ('DIS', 'disable'),
        ('TCK', 'tocheck')
    ]

    state = models.CharField(choices=_STATE_CHOICES,
                             max_length=3, default='TCK')

    def __str__(self) -> str:
        return self.state + " # " + self.select_type + " ### " + self.value

    def save(self, *args, **kwargs):
        if self.value:
            self.normalized_value = SelectValue.normalize(self.value)
        super().save(*args, **kwargs)

    @staticmethod
    def normalize(value: str) -> str:
        value = value.lower()
        value = unicodedata.normalize('NFKD', value).encode(
            'ASCII', 'ignore').decode('ASCII')
        return value

    @staticmethod
    def get_or_create_by_value_many(select_type: str, select_values: list[str]):

        return_array: list[tuple[SelectValue, bool]] = []

        for value in select_values:

            model, created = SelectValue.objects.get_or_create(
                select_type=select_type,
                value=value)
            return_array.append((model, created))

        return return_array


class Paciente(models.Model):

    nome = models.CharField(max_length=128)

    pseudonimo = models.CharField(max_length=128)

    data_nascimento = models.DateField()

    genero = models.ManyToManyField(
        SelectValue, blank=True, related_name='none+', limit_choices_to={'select_type': 'GENER'})
    orientacao_sexual = models.ManyToManyField(
        SelectValue, blank=True, related_name='none+', limit_choices_to={'select_type': 'ORIEN'})
    religiao = models.ManyToManyField(
        SelectValue, blank=True, related_name='none+', limit_choices_to={'select_type': 'RELIG'})
    alergias = models.ManyToManyField(
        SelectValue, blank=True, related_name='none+', limit_choices_to={'select_type': 'ALERG'})

    ja_fez_psicoterapia = models.BooleanField()
    ja_fez_psiquiatrico = models.BooleanField()
    ja_fez_tratamento_espirita = models.BooleanField()

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

    complemento = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.cidade + self.bairro


class NumeroDeTelefone(models.Model):

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    rotulo = models.CharField(max_length=16)

    ddd = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    telefone = models.CharField(max_length=16)

    whatsapp = models.BooleanField()
    telegram = models.BooleanField()
    ligacao = models.BooleanField()

    def __str__(self) -> str:
        return self.paciente.__str__() + '#'+self.ddd+self.telefone


class Email(models.Model):

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    email = models.CharField(max_length=128)


class SolicitacaoAtendimento(models.Model):

    descricao = models.TextField()

    sintomas = models.ManyToManyField(
        SelectValue, blank=True, related_name='none+', limit_choices_to={'select_type': 'SINTO'})

    tratamentos_em_andamento = models.ManyToManyField(
        SelectValue, blank=True, related_name='none+', limit_choices_to={'select_type': 'GENRO'})

    # TODO transformar o bloco abaixo em sintomas tambem?
    # desmaio = models.BooleanField()
    # vulto = models.BooleanField()
    # vozes = models.BooleanField()
    # pensamentos_suicidas = models.BooleanField()
    # desencarne_ultimo_ano = models.BooleanField()

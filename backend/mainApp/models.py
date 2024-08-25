from pyexpat import model
from django.db import models
from django.core.validators import MinLengthValidator

class Options(models.Model):

    value = models.CharField(max_length=256, unique=True)
    normalized_value = models.CharField(max_length=256, unique=True)
    
    STATE_CHOICES = [
        ('enable', 'enable'),
        ('disable', 'disable'),
        ('tocheck', 'tocheck')
    ]

    state = models.CharField(choices=STATE_CHOICES, max_length=8, default='tocheck')

    class Meta:
        abstract = True

# religiao
# genero
# orientacao
# tratamento
# sintoma
# doenca
# alergia
# medicamento

class ReligiaoOptions(Options):
    pass


class GeneroOptions(Options):
    pass


class OrientacaoOptions(Options):
    pass


class TratamentoOptions(Options):
    pass


class SintomaOptions(Options):
    pass


class DoencaOptions(Options):
    pass


class AlergiaOptions(Options):
    pass


class MedicamentoOptions(Options):
    pass



class Paciente(models.Model):

    nome = models.CharField(max_length=128)

    pseudonimo = models.CharField(max_length=128)

    data_nascimento = models.DateField()

    genero = models.ManyToManyField(GeneroOptions)
    orientacao_sexual = models.ManyToManyField(OrientacaoOptions)
    religiao = models.ManyToManyField(ReligiaoOptions)
    alegias = models.ManyToManyField(AlergiaOptions)

    fez_psicoterapia = models.BooleanField()
    fez_psiquiatrico = models.BooleanField()
    fez_tratamento_espirita = models.BooleanField()

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

    tipo_logradouro = models.CharField(max_length=4, choices=TIPOS_LOGRADOURO, default='NDA')

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

    sintomas = models.ManyToManyField(SintomaOptions)

    # TODO transformar o bloco abaixo em sintomas tambem?    
    desmaio = models.BooleanField()
    vulto = models.BooleanField()
    vozes = models.BooleanField()
    pensamentos_suicidas = models.BooleanField()
    desencarne_ultimo_ano = models.BooleanField()

        
    tratamentos_em_andamento = models.ManyToManyField(TratamentoOptions)



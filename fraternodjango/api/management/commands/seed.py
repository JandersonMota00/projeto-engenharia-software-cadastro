from django.core.management.base import BaseCommand
from api.models import SelectValue
from django.core.management import call_command
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Semeia alguns dados no banco de dados'

    def handle(self, *args, **kwargs):
        
        call_command('resetdb')        

        call_command('configpermissions')    



    #Dados iniciais para os selects
    #Gerado pelo GPT, carece verificação        
        data = {
    'RELIG': [
        'Catolicismo', 'Protestantismo', 'Espiritismo', 'Umbanda', 'Candomblé',
        'Budismo', 'Judaísmo', 'Islamismo', 'Xamanismo', 'Confucionismo',
        'Hinduísmo', 'Santo Daime', 'Testemunhas de Jeová', 'Mormonismo', 'Espiritismo'
    ],
    'GENER': [
        'Masculino', 'Feminino', 'Outro', 'Não-binário', 'Transmasculino',
        'Transfeminino', 'Agênero', 'Bigênero', 'Genderqueer', 'Pangênero',
        'Demiboy', 'Demigirl', 'Genderfluid', 'Andrógino', 'Cisgênero'
    ],
    'ORIEN': [
        'Heterossexual', 'Homossexual', 'Bissexual', 'Assexual', 'Pansexual',
        'Demissexual', 'Sapiossexual', 'Greysexual', 'Polissexual', 'Queer',
        'Autosexual', 'Reciprocamente Assexual', 'Androsexual', 'Gynesexual', 'Skoliosexual'
    ],
    'TRATA': [
        'Psicoterapia', 'Psicanálise', 'Tratamento Espiritual', 'Acupuntura', 'Homeopatia',
        'Fisioterapia', 'Osteopatia', 'Naturopatia', 'Terapia Ocupacional', 'Medicina Integrativa',
        'Terapia Cognitivo-Comportamental', 'Tratamento com Medicamentos', 'Terapia de Casal', 'Terapia Familiar', 'Terapia Floral'
    ],
    'SINTO': [
        'Ansiedade', 'Depressão', 'Pânico', 'Insônia', 'Stress',
        'Tristeza', 'Irritabilidade', 'Medo', 'Agitação', 'Euforia',
        'Fadiga', 'Apatia', 'Desesperança', 'Dúvida', 'Dificuldade de Concentração'
    ],
    'DOENC': [
        'Diabetes', 'Hipertensão', 'Asma', 'Gastrite', 'Artrite',
        'Colesterol Alto', 'Doença Cardíaca', 'Enxaqueca', 'Sinusite', 'Refluxo',
        'Bronquite', 'Câncer', 'Doença Pulmonar Obstrutiva Crônica', 'Doença Autoimune', 'Hipotireoidismo'
    ],
    'ALERG': [
        'Pólen', 'Leite', 'Amendoim', 'Penicilina', 'Ácaros',
        'Frutos do Mar', 'Ovo', 'Glúten', 'Nozes', 'Grãos',
        'Soja', 'Lactose', 'Café', 'Chocolate', 'Rinites'
    ],
    'MEDIC': [
        'Paracetamol', 'Ibuprofeno', 'Dipirona', 'Amoxicilina', 'Azitromicina',
        'Loratadina', 'Cetirizina', 'Metformina', 'Losartana', 'Enalapril',
        'Omeprazol', 'Simvastatina', 'Prednisona', 'Dextrometorfano'
    ]
}


        #  desmaio
        # vulto
        # vozes
        # pensamentos_suicidas
        # desencarne_ultimo_ano

        data['SINTO'].extend(['Desmaio', 'Vultos', 'Vozes', 'Pensamentos suicidas', 'Desencarne familiar'])

        # Itera sobre cada tipo de select_name e seus valores
        for select_type, select_type_values in data.items():
            for value in select_type_values:
                normalized_value = value.lower().replace(' ', '_')
                # Verifica se o valor já existe antes de criar
                if not SelectValue.objects.filter(select_type=select_type, value=value).exists():
                    SelectValue.objects.create(
                        select_type=select_type,
                        value=value,
                        state='ENA'  # Assume que 'ENA' é o código para 'enable'
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'Sucesso ao adicionar: {select_type} - {value}'))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Já existe: {select_type} - {value}'))

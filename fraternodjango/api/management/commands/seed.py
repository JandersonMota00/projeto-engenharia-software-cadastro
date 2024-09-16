from django.core.management.base import BaseCommand
from api.models import (
    ReligiaoValue, GeneroValue, OrientacaoSexualValue,
    TratamentoValue, SintomaValue, DoencaValue,
    AlergiaValue, MedicamentoValue, BaseSelectValue
)
from django.core.management import call_command
from django.db.models import Model


class Command(BaseCommand):
    help = 'Semeia alguns dados no banco de dados'

    def handle(self, *args, **kwargs):
        
        # Dados iniciais para os selects
        data = {
            'religiao': [
                'Catolicismo', 'Protestantismo', 'Espiritismo', 'Umbanda', 'Candomblé',
                'Budismo', 'Judaísmo', 'Islamismo', 'Xamanismo', 'Confucionismo',
                'Hinduísmo', 'Santo Daime', 'Testemunhas de Jeová', 'Mormonismo', 'Espiritismo'
            ],
            'genero': [
                'Masculino', 'Feminino', 'Outro', 'Não-binário', 'Transmasculino',
                'Transfeminino', 'Agênero', 'Bigênero', 'Genderqueer', 'Pangênero',
                'Demiboy', 'Demigirl', 'Genderfluid', 'Andrógino', 'Cisgênero'
            ],
            'orientacao_sexual': [
                'Heterossexual', 'Homossexual', 'Bissexual', 'Assexual', 'Pansexual',
                'Demissexual', 'Sapiossexual', 'Greysexual', 'Polissexual', 'Queer',
                'Autosexual', 'Reciprocamente Assexual', 'Androsexual', 'Gynesexual', 'Skoliosexual'
            ],
            'tratamento': [
                'Psicoterapia', 'Psicanálise', 'Tratamento Espiritual', 'Acupuntura', 'Homeopatia',
                'Fisioterapia', 'Osteopatia', 'Naturopatia', 'Terapia Ocupacional', 'Medicina Integrativa',
                'Terapia Cognitivo-Comportamental', 'Tratamento com Medicamentos', 'Terapia de Casal', 'Terapia Familiar', 'Terapia Floral'
            ],
            'sintoma': [
                'Ansiedade', 'Depressão', 'Pânico', 'Insônia', 'Stress',
                'Tristeza', 'Irritabilidade', 'Medo', 'Agitação', 'Euforia',
                'Fadiga', 'Apatia', 'Desesperança', 'Dúvida', 'Dificuldade de Concentração',
                'Desmaio', 'Vultos', 'Vozes', 'Pensamentos suicidas', 'Desencarne familiar'
            ],
            'doenca': [
                'Diabetes', 'Hipertensão', 'Asma', 'Gastrite', 'Artrite',
                'Colesterol Alto', 'Doença Cardíaca', 'Enxaqueca', 'Sinusite', 'Refluxo',
                'Bronquite', 'Câncer', 'Doença Pulmonar Obstrutiva Crônica', 'Doença Autoimune', 'Hipotireoidismo'
            ],
            'alergia': [
                'Pólen', 'Leite', 'Amendoim', 'Penicilina', 'Ácaros',
                'Frutos do Mar', 'Ovo', 'Glúten', 'Nozes', 'Grãos',
                'Soja', 'Lactose', 'Café', 'Chocolate', 'Rinites'
            ],
            'medicamento': [
                'Paracetamol', 'Ibuprofeno', 'Dipirona', 'Amoxicilina', 'Azitromicina',
                'Loratadina', 'Cetirizina', 'Metformina', 'Losartana', 'Enalapril',
                'Omeprazol', 'Simvastatina', 'Prednisona', 'Dextrometorfano'
            ]
        }

        model_mapping = {
            'religiao': ReligiaoValue,
            'genero': GeneroValue,
            'orientacao_sexual': OrientacaoSexualValue,
            'tratamento': TratamentoValue,
            'sintoma': SintomaValue,
            'doenca': DoencaValue,
            'alergia': AlergiaValue,
            'medicamento': MedicamentoValue,
        }

        # Itera sobre cada tipo de select_name e seus valores
        for select_type, select_type_values in data.items():
            model_class: Model = model_mapping[select_type]
            for value in select_type_values:
                
                normalized_value = BaseSelectValue.normalize(value)
                # Verifica se o valor já existe antes de criar
                if not model_class.objects.filter(value=value).exists():
                    model_class.objects.create(
                        value=value,
                        state='ENA'  # Assume que 'ENA' é o código para 'enable'
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'Sucesso ao adicionar: {select_type} - {value}'))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'Já existe: {select_type} - {value}'))

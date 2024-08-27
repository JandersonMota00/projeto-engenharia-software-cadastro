from django import forms
from .models import Paciente, SelectValue
from mainApp.models import Paciente, SelectValue, Endereco, NumeroDeTelefone, Email

class SelectValueForm(forms.ModelForm):
    class Meta:
        model = SelectValue
        fields = ['select_type', 'value', 'state']

    def save(self, commit=True):
        # Chamamos a lógica de normalização antes de salvar
        if self.instance.value:
            self.instance.normalized_value = SelectValue.normalize(self.instance.value)
        return super().save(commit=commit)

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep', 'estado', 'cidade', 'bairro', 'tipo_logradouro', 'logradouro', 'numero', 'complemento']

class NumeroDeTelefoneForm(forms.ModelForm):
    class Meta:
        model = NumeroDeTelefone
        fields = ['rotulo', 'ddd', 'telefone', 'whatsapp', 'telegram', 'ligacao']

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email']

class PacienteForm(forms.ModelForm):
    
    SelectFormFieldName_To_SelectType = {
        'genero': 'GENER',
        'orientacao_sexual': 'ORIEN',
        'religiao': 'RELIG',
        'alergias': 'ALERG',
    }
    
    # enderecos = forms.JSONField(required=False)
    # telefones = forms.JSONField(required=False)
    # emails = forms.JSONField(required=False)

    class Meta:
        model = Paciente
        fields = ['nome', 'pseudonimo', 'data_nascimento', 'genero', 'orientacao_sexual', 'religiao', 'alergias',
                  'ja_fez_psicoterapia', 'ja_fez_psiquiatrico', 'ja_fez_tratamento_espirita']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['genero'].queryset = SelectValue.objects.filter(select_type='GENER')
        self.fields['orientacao_sexual'].queryset = SelectValue.objects.filter(select_type='ORIEN')
        self.fields['religiao'].queryset = SelectValue.objects.filter(select_type='RELIG')
        self.fields['alergias'].queryset = SelectValue.objects.filter(select_type='ALERG')


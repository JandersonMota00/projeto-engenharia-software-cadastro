from django import forms
from .models import Paciente, SelectValue
from mainApp.models import Paciente, SelectValue


class PacienteForm(forms.ModelForm):

    SelectFormFieldName_To_SelectType = {
        'genero': 'GENER',
        'orientacao_sexual': 'ORIEN',
        'religiao': 'RELIG',
        'alergias': 'ALERG',
    }



    class Meta:
        model = Paciente
        fields = ['nome', 'pseudonimo', 'data_nascimento', 'genero', 'orientacao_sexual', 'religiao', 'alergias',
                  'ja_fez_psicoterapia', 'ja_fez_psiquiatrico', 'ja_fez_tratamento_espirita']

    def __init__(self, *args, **kwargs):

        mutable_args = list(args)
        
        mutable_args[0] = self.args_selectValues_To_selectPKs(mutable_args[0])    
        
        print('mutable', mutable_args[0])
        
        super().__init__(*mutable_args, **kwargs)
        
        
        self.fields['genero'].queryset = SelectValue.objects.filter(select_type='GENER')
        self.fields['orientacao_sexual'].queryset = SelectValue.objects.filter(select_type='ORIEN')
        self.fields['religiao'].queryset = SelectValue.objects.filter(select_type='RELIG')
        self.fields['alergias'].queryset = SelectValue.objects.filter(select_type='ALERG')


    def args_selectValues_To_selectPKs(self, data: dict):
        
        #iremos extrair os campos selects para a variavel abaixo
        
        return_data: dict[str, list[int]] = {}
        
        for formfieldname in PacienteForm.SelectFormFieldName_To_SelectType:
            
            #iremos converter os values em instancias e salvar na variavel abaixo
            
            for values in data.get(formfieldname, []):
                                
                instances_and_created = SelectValue.get_or_create_by_value_many(
                    select_type=formfieldname, select_values=values)

                instances = [instance for instance, created in instances_and_created]
                
                return_data[formfieldname] = []
                
                for instance in instances:
                    return_data[formfieldname].append(instance.id)
        
        
        data.update(return_data)

        return data
     
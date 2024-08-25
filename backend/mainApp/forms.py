from django import forms



class CreatePacienteForm(forms.Form):
    
    nome = forms.CharField()


from django.contrib import admin

from mainApp.models import Email, Endereco, NumeroDeTelefone, Paciente, SelectValue, SolicitacaoAtendimento
# Register your models here.


admin.site.register(Paciente)
admin.site.register(Endereco)
admin.site.register(NumeroDeTelefone)
admin.site.register(Email)
admin.site.register(SolicitacaoAtendimento)
admin.site.register(SelectValue)

# religiao
# genero
# orientacao
# tratamento
# sintoma
# doenca
# alergia
# medicamento

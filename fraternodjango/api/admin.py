from django.contrib import admin

from .models import (Endereco, NumeroDeTelefone, Paciente, SolicitacaoAtendimento)
                    
# Register your models here.


admin.site.register(Paciente)
admin.site.register(Endereco)
admin.site.register(NumeroDeTelefone)
admin.site.register(SolicitacaoAtendimento)


# religiao
# genero
# orientacao
# tratamento
# sintoma
# doenca
# alergia
# medicamento

from django.contrib import admin

from api.models import (Email, Endereco, NumeroDeTelefone, Paciente, SolicitacaoAtendimento, GeneroValue,
                        OrientacaoSexualValue, ReligiaoValue, AlergiaValue, SintomaValue, TratamentoValue,
                        DoencaValue, MedicamentoValue,)
# Register your models here.


admin.site.register(Paciente)
admin.site.register(Endereco)
admin.site.register(NumeroDeTelefone)
admin.site.register(Email)
admin.site.register(SolicitacaoAtendimento)

admin.site.register(ReligiaoValue)
admin.site.register(GeneroValue)
admin.site.register(OrientacaoSexualValue)
admin.site.register(TratamentoValue)
admin.site.register(SintomaValue)
admin.site.register(DoencaValue)
admin.site.register(AlergiaValue)
admin.site.register(MedicamentoValue)

# religiao
# genero
# orientacao
# tratamento
# sintoma
# doenca
# alergia
# medicamento

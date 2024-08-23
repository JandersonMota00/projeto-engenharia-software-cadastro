from django.contrib import admin

from mainApp.models import AlergiaOptions, DoencaOptions, Email, Endereco, GeneroOptions, MedicamentoOptions, NumeroDeTelefone, OrientacaoOptions, Paciente, ReligiaoOptions, SintomaOptions, TratamentoOptions
# Register your models here.


admin.site.register(Paciente)
admin.site.register(Endereco)
admin.site.register(NumeroDeTelefone)
admin.site.register(Email)

# religiao
# genero
# orientacao
# tratamento
# sintoma
# doenca
# alergia
# medicamento

admin.site.register(ReligiaoOptions)
admin.site.register(GeneroOptions)
admin.site.register(OrientacaoOptions)
admin.site.register(TratamentoOptions)
admin.site.register(SintomaOptions)
admin.site.register(DoencaOptions)
admin.site.register(AlergiaOptions)
admin.site.register(MedicamentoOptions)
from django.contrib import admin

# Register your models here.

from .models import (
    GeneroValue, OrientacaoSexualValue, ReligiaoValue,
    AlergiaValue, SintomaValue, TratamentoValue,
    DoencaValue, MedicamentoValue,)

admin.site.register(ReligiaoValue)
admin.site.register(GeneroValue)
admin.site.register(OrientacaoSexualValue)
admin.site.register(TratamentoValue)
admin.site.register(SintomaValue)
admin.site.register(DoencaValue)
admin.site.register(AlergiaValue)
admin.site.register(MedicamentoValue)

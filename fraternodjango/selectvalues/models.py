from django.db import models

import unicodedata

class BaseSelectValue(models.Model):
    
    value = models.CharField(max_length=256)
    
    normalized_value = models.CharField(max_length=256, editable=False)
    
    state = models.CharField(choices=[
        ('enable', 'enable'),
        ('disable', 'disable'),
        ('tocheck', 'tocheck')
    ], max_length=8, default='tocheck')

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.state} ### {self.value} # {self.id}"

    def save(self, *args, **kwargs):
        if self.value:
            self.normalized_value = self.normalize(self.value)
        super().save(*args, **kwargs)

    @staticmethod
    def normalize(value: str) -> str:
        value = value.lower()
        value = unicodedata.normalize('NFKD', value).encode(
            'ASCII', 'ignore').decode('ASCII')
        return value

# Modelos especializados para cada tipo de SelectValue

class ReligiaoValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Religião'
        verbose_name_plural = 'Religiões'

class GeneroValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'

class OrientacaoSexualValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Orientação Sexual'
        verbose_name_plural = 'Orientações Sexuais'

class TratamentoValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Tratamento'
        verbose_name_plural = 'Tratamentos'

class SintomaValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Sintoma'
        verbose_name_plural = 'Sintomas'

class DoencaValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Doença'
        verbose_name_plural = 'Doenças'

class AlergiaValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Alergia'
        verbose_name_plural = 'Alergias'

class MedicamentoValue(BaseSelectValue):
    class Meta(BaseSelectValue.Meta):
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'


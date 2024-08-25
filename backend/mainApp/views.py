from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from mainApp import models

# Create your views here.


def getOptions(request: HttpRequest, selectname: str, searchterm: str):

    match selectname:
        case 'religiao':
            # Código específico para religiao
            return JsonResponse(models.ReligiaoOptions.objects.filter())
        case 'genero':
            # Código específico para genero
            pass
        case 'orientacao':
            # Código específico para orientacao
            pass
        case 'tratamento':
            # Código específico para tratamento
            pass
        case 'sintoma':
            # Código específico para sintoma
            pass
        case 'doenca':
            # Código específico para doenca
            pass
        case 'alergia':
            # Código específico para alergia
            pass
        case 'medicamento':
            # Código específico para medicamento
            pass
        case _:
            # Código para o caso default, se nenhum dos acima corresponder
            pass

    return HttpResponse()


def home(r: HttpRequest):
    return HttpResponse(render(r, ''))


def createPaciente(r: HttpRequest):

    pass


def seed(request: HttpRequest):

    # religiao
    # genero
    # orientacao
    # tratamento
    # sintoma
    # doenca
    # alergia
    # medicamento

    models.ReligiaoOptions(value='test').save()

    models.GeneroOptions(value='test').save()
    models.OrientacaoOptions(value='test').save()
    models.TratamentoOptions(value='test').save()
    models.SintomaOptions(value='test').save()
    models.DoencaOptions(value='test').save()
    models.AlergiaOptions(value='test').save()
    models.MedicamentoOptions(value='test').save()

    return HttpResponse('seeded')

from django.http import HttpRequest, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from mainApp.models import Paciente, SelectValue
from mainApp.forms import PacienteForm
import json

from mainApp import models

# Create your views here.


class SearchSelectValueView(View):
    def get(self, request):
        # Obtém os parâmetros GET
        select_type = request.GET.get('select_type')
        search_value = request.GET.get('search_value')

        # Verifica se os parâmetros estão presentes
        if not select_type or not search_value:
            return JsonResponse({'error': 'Parâmetros `select_name` e `search_value` são obrigatórios.'}, status=400)

        # Filtra os registros no modelo SelectValue com base no select_name
        results = models.SelectValue.objects.filter(
            select_type__exact=select_type,

            normalized_value__icontains=models.SelectValue.normalize(
                search_value)
        ).order_by('value')[:10]  # Limita os resultados a 10

        # Converte os resultados em uma lista de dicionários para o JSON
        results_list = [{'id': result.id, 'value': result.value}
                        for result in results]

        # Retorna os resultados como JSON
        return JsonResponse(results_list, safe=False)


# TODO achar uma maneira melhor em vez de desbalitar csrf
@method_decorator(csrf_exempt, name='dispatch')
class PacienteCreateView(View):
    def post(self, request):
        import json

        # Converte o corpo da requisição JSON para um dicionário
        data = json.loads(request.body)


        # Prepara os dados para o formulário


        form = PacienteForm(data)

        if form.is_valid():
            paciente = form.save()

            response_data = {
                'id': paciente.id,
                'nome': paciente.nome,
                'pseudonimo': paciente.pseudonimo,
                'data_nascimento': paciente.data_nascimento.isoformat(),
            }
                           
            # Retorna uma resposta JSON com status 201 (Created)
            return JsonResponse(response_data, status=201)
        else:
            # Retorna erros de validação com status 400 (Bad Request)
            return JsonResponse(form.errors, status=400)

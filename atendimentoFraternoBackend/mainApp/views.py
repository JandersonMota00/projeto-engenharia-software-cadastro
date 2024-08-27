from django.http import HttpRequest, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from mainApp.models import SelectValue
from mainApp.forms import EmailForm, NumeroDeTelefoneForm, PacienteForm, SelectValueForm, EnderecoForm
import json
from django.shortcuts import get_object_or_404
from django.db import transaction


# Create your views here.

# TODO achar uma maneira melhor em vez de desbalitar csrf
@method_decorator(csrf_exempt, name='dispatch')
class SelectValueView(View):
    
    def get(self, request: HttpRequest):
        
        # Obtém os parâmetros GET
        select_type = request.GET.get('select_type')
        search_term = request.GET.get('search_term')

        # Verifica se os parâmetros estão presentes
        if not select_type or not search_term:
            return JsonResponse({'error': 'Parâmetros `select_name` e `search_term` são obrigatórios.'}, status=400)

        normalized_search_term = SelectValue.normalize(search_term)
        
        # Filtra os registros no modelo SelectValue com base no select_name
        values = SelectValue.objects.filter(
            select_type=select_type,
            normalized_value__icontains=normalized_search_term,
            state='ENA'
        )[:10]  # Limita a 10 resultados

        # Converte os resultados em uma lista de dicionários para o JSON
        response_data = [
            {
             'id': value.id,
             'value': value.value, 
             }
            for value in values
        ]
        
        # Retorna os resultados como JSON
        return JsonResponse(response_data, safe=False)

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        select_value_id = data.get('id')

        if select_value_id:
            # Tentar obter o objeto existente
            select_value = get_object_or_404(SelectValue, id=select_value_id)
            form = SelectValueForm(data, instance=select_value)
        else:
            # Criar um novo objeto
            form = SelectValueForm(data)

        if form.is_valid():
            select_value = form.save()
            response_data = {
                'id': select_value.id,
                'select_type': select_value.select_type,
                'value': select_value.value,
                'normalized_value': select_value.normalized_value,
                'state': select_value.state
            }
            return JsonResponse(response_data, status=200 if select_value_id else 201)
        else:
            return JsonResponse(form.errors, status=400)


# TODO achar uma maneira melhor em vez de desbalitar csrf
@method_decorator(csrf_exempt, name='dispatch')
class PacienteCreateView(View):
     def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
                
        paciente_data = data.get('paciente', {})
        endereco_data = data.get('enderecos', {})
        telefones_data = data.get('telefones', [])
        emails_data = data.get('emails', [])
        
        # Criar os formulários
        paciente_form = PacienteForm(paciente_data)
        endereco_form = EnderecoForm(endereco_data)
        
        telefone_forms = [NumeroDeTelefoneForm(telefone_data) for telefone_data in telefones_data]
        email_forms = [EmailForm(email_data) for email_data in emails_data]
        
        # Verificar se todos os formulários são válidos
        forms_valid = (
            paciente_form.is_valid() and 
            endereco_form.is_valid() and 
            all(telefone_form.is_valid() for telefone_form in telefone_forms) and 
            all(email_form.is_valid() for email_form in email_forms)
        )

        if forms_valid:
            try:
                with transaction.atomic():
                    paciente = paciente_form.save()

                    # Salvar endereço
                    endereco = endereco_form.save(commit=False)
                    endereco.paciente = paciente
                    endereco.save()

                    # Salvar telefones
                    for telefone_form in telefone_forms:
                        telefone = telefone_form.save(commit=False)
                        telefone.paciente = paciente
                        telefone.save()

                    # Salvar emails
                    for email_form in email_forms:
                        email = email_form.save(commit=False)
                        email.paciente = paciente
                        email.save()

                return JsonResponse({"status": "success", "paciente_id": paciente.id}, status=201)

            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=500)
        else:
            errors = {
                "paciente_errors": paciente_form.errors,
                "endereco_errors": endereco_form.errors,
                "telefone_errors": [telefone_form.errors for telefone_form in telefone_forms],
                "email_errors": [email_form.errors for email_form in email_forms],
            }
            return JsonResponse({"status": "error", "errors": errors}, status=400)
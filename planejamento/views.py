from django.shortcuts import render
from perfil.models import Categoria, Conta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required


@login_required(login_url='/auth/logar/')
def definir_planejamento(request):
    user = request.user
    categorias = Categoria.objects.filter(user=user)
    return render(request, 'definir_planejamento.html', {'categorias': categorias})



@login_required(login_url='/auth/logar/')
@csrf_exempt
def update_valor_categoria(request, id):
    user = request.user
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(user=user, id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()

    return JsonResponse({'status': 'Sucesso'})

@login_required(login_url='/auth/logar/')
def ver_planejamento(request):
    user = request.user
    categorias = Categoria.objects.filter(user=user)
    return render(request, 'ver_planejamento.html', {'categorias': categorias})
from django.shortcuts import render, redirect
from perfil.models import Categoria, Conta
from contas.models import ContaPagar, ContaPaga
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/logar/')
def definir_contas(request):
    user = request.user
    
    if request.method == "GET":
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html', {'categorias': categorias})
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        conta = ContaPagar(
            user=user,
            titulo=titulo,
            categoria_id=categoria,
            descricao=descricao,
            valor=valor,
            dia_pagamento=dia_pagamento
        )

        conta.save()

        messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
        return redirect('/contas/definir_contas')
    
@login_required(login_url='/auth/logar/')
def ver_contas(request):
    user = request.user
    
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    
    contas = ContaPagar.objects.filter(user=user)

    contas_pagas = ContaPaga.objects.filter(conta__user=user, data_pagamento__month=MES_ATUAL).values('conta')

    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte=DIA_ATUAL + 5, dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
    
    restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_pagas).exclude(id__in=contas_proximas_vencimento)

    return render(request, 'ver_contas.html', {
        'contas_vencidas': contas_vencidas, 
        'contas_proximas_vencimento': contas_proximas_vencimento, 
        'restantes': restantes, 
        'contas_pagas': contas_pagas,
    })

@login_required(login_url='/auth/logar/')
def pagar_conta(request, conta_id):
    user = request.user
    
    conta = ContaPagar.objects.get(pk=conta_id, user=user)
    conta_paga = ContaPaga(conta=conta, data_pagamento=datetime.now(), user=user)
    conta_paga.save()
    messages.add_message(request, constants.SUCCESS, 'Conta marcada como paga')
    return redirect('/contas/ver_contas')

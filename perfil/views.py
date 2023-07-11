from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total, calcula_equilibrio_financeiro
from django.db.models import Sum
from extrato.models import Valores
from datetime import datetime, timedelta
from contas.models import ContaPagar, ContaPaga
from contas.views import ver_contas
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

@login_required
def home(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    
    user = request.user
    
    # Filtrar valores do usuário atual
    valores = Valores.objects.filter(user=user, data__month=datetime.now().month)
    
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')   
    total_livre = total_entradas - total_saidas

    # Filtrar contas do usuário atual
    contas = Conta.objects.filter(user=user)

    total_contas = calcula_total(contas, 'valor')

    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()

    contas_proximas_vencimento = ver_contas(request)

    contas_vencidas = ver_contas(request)

    return render(request, 'home.html', {
        'contas': contas,
        'total_contas': total_contas,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'percentual_gastos_essenciais': int(percentual_gastos_essenciais),
        'percentual_gastos_nao_essenciais': int(percentual_gastos_nao_essenciais),
        'total_livre': total_livre, 
        'contas_vencidas': contas_vencidas,
        'contas_proximas_vencimento': contas_proximas_vencimento,
    })



@login_required
def gerenciar(request):
    user = request.user
    contas = Conta.objects.filter(user=user)
    categorias = Categoria.objects.filter(user=user)

    total_contas = calcula_total(contas, 'valor')

    return render(request, 'gerenciar.html', {'contas': contas, 'total_contas': total_contas, 'categorias': categorias})


@login_required
def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
        return redirect('/perfil/gerenciar/')

    user = request.user  # Obter o usuário atualmente logado
    conta = Conta(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone,
        user=user,  # Atribuir o usuário atual ao campo 'user'
    )

    conta.save()

    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
    return redirect('/perfil/gerenciar/')

    
@login_required
def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return redirect('/perfil/gerenciar/')


@login_required
def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    if len(nome.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Crie um nome para categoria! Não deixe o campo em branco.')
        return redirect('/perfil/gerenciar/')
        
    user = request.user

    categoria = Categoria(
        categoria=nome,
        essencial=essencial, 
        user=user,
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')


@login_required
def update_categoria(request, id):
    user = request.user

    try:
        categoria = Categoria.objects.get(id=id, user=user)
    except Categoria.DoesNotExist:
        # Lidar com a categoria não encontrada
        return redirect('/perfil/gerenciar/')
    
    categoria.essencial = not categoria.essencial
    categoria.save()

    return redirect('/perfil/gerenciar/')


@login_required
def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        # Filtrar os valores do usuário atual e da categoria atual
        valores = Valores.objects.filter(user=request.user, categoria=categoria)
        total_valor = valores.aggregate(Sum('valor'))['valor__sum']
        dados[categoria.categoria] = total_valor or 0

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})

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

def home(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')   
    total_livre = total_entradas - total_saidas

    contas = Conta.objects.all()

    total_contas = calcula_total(contas, 'valor')

    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()

    contas_vencidas = ver_contas(request)

    

    return render(request, 'home.html', {'contas': contas,
                                         'total_contas': total_contas,
                                         'total_entradas': total_entradas,
                                         'total_saidas': total_saidas,
                                         'percentual_gastos_essenciais': int(percentual_gastos_essenciais),
                                         'percentual_gastos_nao_essenciais': int(percentual_gastos_nao_essenciais),
                                         'total_livre': total_livre, 
                                         'contas_vencidas': contas_vencidas
                                         })


def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    total_contas = calcula_total(contas, 'valor')

    return render(request, 'gerenciar.html', {'contas': contas, 'total_contas': total_contas, 'categorias': categorias})


def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
        return redirect('/perfil/gerenciar/')

    conta = Conta(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone,
    )

    conta.save()

    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
    return redirect('/perfil/gerenciar/')

    
def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    if len(nome.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Crie um nome para categoria! Não deixe o campo em branco.')
        return redirect('/perfil/gerenciar/')
        

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')


def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()

    return redirect('/perfil/gerenciar/')


def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        dados[categoria.categoria] = Valores.objects.filter(categoria=categoria).aggregate(Sum('valor'))['valor__sum']

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})
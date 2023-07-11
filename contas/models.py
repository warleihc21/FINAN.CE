from django.db import models
from perfil.models import Categoria
from django.contrib.auth.models import User
from django.utils import timezone

class ContaPagar(models.Model):
    titulo = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    valor = models.FloatField()
    dia_pagamento = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.titulo
    

class ContaPaga(models.Model):
    conta = models.ForeignKey(ContaPagar, on_delete=models.DO_NOTHING)
    data_pagamento = models.DateField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

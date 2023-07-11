from django.db import models
from perfil.models import Categoria, Conta
from django.contrib.auth.models import User

class Valores(models.Model):
    choice_tipo = (
        ('E', 'Entrada'),
        ('S', 'Saída')
    )
    
    valor = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    data = models.DateField()
    conta = models.ForeignKey(Conta, on_delete=models.DO_NOTHING)
    tipo = models.CharField(max_length=1, choices=choice_tipo)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.descricao

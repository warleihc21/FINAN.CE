from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

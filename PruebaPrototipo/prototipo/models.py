from django.db import models



class Formulario(models.Model):

    campoPalabra = models.CharField(max_length=200)
    ordering = ('campoPalabra',)

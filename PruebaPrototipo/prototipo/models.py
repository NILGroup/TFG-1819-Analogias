from django.db import models



class Formulario(models.Model):

    campoPalabra = models.CharField(max_length=200)
    ordering = ('campoPalabra',)



class FormularioTerminos(models.Model):

    Palabra = models.CharField(max_length=200)
    ordering = ('Palabra',)


class FormularioFinal(models.Model):

    Word = models.CharField(max_length=200)
    Depth = models.IntegerField(default=1)
    ordering = ('Word', 'Depth')
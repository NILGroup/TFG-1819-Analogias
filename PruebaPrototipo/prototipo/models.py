from django.db import models



class Formulario(models.Model):

    campoPalabra = models.CharField(max_length=200)
    ordering = ('campoPalabra',)



class FormularioTerminos(models.Model):

    Palabra = models.CharField(max_length=200)
    ordering = ('Palabra',)


class FormularioFinal(models.Model):

    PalabraABuscar = models.CharField(max_length=200)
    Profundidad = models.IntegerField(default=1)
    ordering = ('PalabraABuscar', 'Profundidad')
from django.db import models


''' 
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

'''

class WeiSpa30Variant(models.Model):
    word = models.CharField(primary_key=True, max_length=100)
    sense = models.IntegerField()
    offset = models.CharField(max_length=17)
    pos = models.CharField(max_length=1)
    csco = models.FloatField()
    experiment = models.CharField(max_length=20, blank=True, null=True)
    mark = models.CharField(max_length=20)
    palabra = models.CharField(max_length=200)
    ordering = ('word',)


    class Meta:
        managed = False
        db_table = 'wei_spa-30_variant'
        unique_together = (('word', 'sense', 'pos', 'offset'),)

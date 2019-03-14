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
   #palabra = models.CharField(max_length=200)
    ordering = ('word',)


    class Meta:
        managed = False
        db_table = 'wei_spa-30_variant'
        unique_together = (('word', 'sense', 'pos', 'offset'),)





class WeiSpa30Relation(models.Model):
    relation = models.SmallIntegerField(primary_key=True)
    sourcesynset = models.CharField(db_column='sourceSynset', max_length=17)  # Field name made lowercase.
    sourcepos = models.CharField(db_column='sourcePos', max_length=1)  # Field name made lowercase.
    targetsynset = models.CharField(db_column='targetSynset', max_length=17)  # Field name made lowercase.
    targetpos = models.CharField(db_column='targetPos', max_length=1)  # Field name made lowercase.
    csco = models.FloatField()
    method = models.CharField(max_length=2)
    version = models.CharField(max_length=1)
    wnsource = models.CharField(db_column='wnSource', max_length=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wei_spa-30_relation'
        unique_together = (('relation', 'sourcesynset', 'sourcepos', 'targetsynset', 'targetpos', 'method', 'version', 'wnsource'),)



class WeiSpa30Synset(models.Model):
    offset = models.CharField(primary_key=True, max_length=17)
    pos = models.CharField(max_length=1)
    sons = models.IntegerField()
    status = models.CharField(max_length=1)
    lexical = models.CharField(max_length=1)
    instance = models.IntegerField()
    gloss = models.TextField(blank=True, null=True)
    level = models.IntegerField()
    levelfromtop = models.IntegerField(db_column='levelFromTop')  # Field name made lowercase.
    mark = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'wei_spa-30_synset'
        unique_together = (('offset', 'pos'),)

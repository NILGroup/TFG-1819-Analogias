from django.shortcuts import render
from collections import defaultdict
import requests
import csv
import nltk
import os
import json
from django.http import HttpResponse

from nltk.corpus import wordnet as wn


from django.shortcuts import redirect

from .models import WeiSpa30Variant, WeiSpa30Relation
from .forms import PostFormWordSearch


def index(request):
    form = PostFormWordSearch()


    if request.method == "POST":
        form = PostFormWordSearch(request.POST)

        if 'boton-final' in request.POST:

            word = form['word'].value()
            resultadoSinonimos, resultadoHiponimo, resultadoHiperonimo = busquedaDePalabras(word)

            dict_resultados = dict(sinonimos="", hiponimos="", hiperonimos="")

            dict_resultados["sinonimos"] = list(busquedaSinonimosEnLaRAE(resultadoSinonimos))
            dict_resultados["hiponimos"] = list(busquedaHiponimosEnLaRAE(resultadoHiponimo))
            dict_resultados["hiperonimos"] = list(busquedaHiperonimosEnLaRAE(resultadoHiperonimo))


            return render(request, 'prototipo/formulario.html', {'form': form,'resultadoSinonimos' : resultadoSinonimos, 'resultadoHiponimo' : resultadoHiponimo, 'resultadoHiperonimo' : resultadoHiperonimo, 'word' : word, 'dict' : dict_resultados, 'json': json.dumps(dict_resultados, ensure_ascii=False)})


    return render(request, 'prototipo/formulario.html', {'form': form })





########################################################################################################################################################

##################      Método que busca que palabras son iguales a la introducida y se queda con su offset para posteriormente saber sus sinónimos
#################       hipónimos e hiperónimos

########################################################################################################################################################

def busquedaDePalabras(word):

    #Primero busca que palabras son iguales a la palabra de entrada y nos quedamos con la columna offset
    palabrasQueCoinciden = WeiSpa30Variant.objects.filter(word=word).only('offset')

    #for indice in palabrasQueCoinciden.values():
        #print(indice.values())

    listaResultadoSinonimos = busquedadSinonimos(palabrasQueCoinciden)

    resultadoHiponimo, resultadoHiperonimo = busquedadHipoHiper(palabrasQueCoinciden)


    return listaResultadoSinonimos, resultadoHiponimo, resultadoHiperonimo





########################################################################################################################################################

##################      Metódo que busca en la misma tabla la palabra, cuyo offset coincide con el offset de la palabra introducida ##################

########################################################################################################################################################

def busquedadSinonimos(palabrasQueCoinciden):

    sinonimosPorCadaSynset = []
    listaResultadoNombres = []
    contador = 0


    for indiceListaPalabras in range(len(palabrasQueCoinciden)):
        sinonimos = WeiSpa30Variant.objects.filter(offset=palabrasQueCoinciden[indiceListaPalabras].offset)

        for indiceLista in sinonimos.values():
            if palabrasQueCoinciden[0].word != indiceLista['word']:
                sinonimosPorCadaSynset.append(indiceLista['word'])

        insertar = sinonimosPorCadaSynset.copy()
        listaResultadoNombres.insert(contador, insertar)
        contador = contador + 1
        sinonimosPorCadaSynset.clear()


    return listaResultadoNombres





########################################################################################################################################################

##################      Metódo que en función de si el offset de la palabra introducida está en la columna sourcesynset o targetsynset,
##################      busca en la columna contraria y lo guarda en una lista ##################

########################################################################################################################################################

def busquedadHipoHiper(palabrasQueCoinciden):
    listaOffsetsSourceFinal = list()
    listaOffsetsTargetFinal = list()

    if len(palabrasQueCoinciden) > 0:

        for offset in range(len(palabrasQueCoinciden)):

            ###########     Hiponimo      ###########
            offsetQueEstaEnSourceSynset = WeiSpa30Relation.objects.filter(sourcesynset=palabrasQueCoinciden[offset].offset) & (WeiSpa30Relation.objects.filter(relation=12))

            for listaOffsets in offsetQueEstaEnSourceSynset.values():
                listaOffsetsSourceFinal.append(listaOffsets['targetsynset'])
                #print(listaOffsets.values())

            #print(len(offsetQueEstaEnSourceSynset))

            ###########     Hiperónimo      ###########

            offsetQueEstaEnTargetSynset = WeiSpa30Relation.objects.filter(targetsynset=palabrasQueCoinciden[offset].offset) & (WeiSpa30Relation.objects.filter(relation=12))

            for listaOffsets in offsetQueEstaEnTargetSynset.values():
                listaOffsetsTargetFinal.append(listaOffsets['sourcesynset'])

                # print(listaOffsets.values())


        listaResultadoHiponimo = busquedaPalabrasQueSonHiponimos(palabrasQueCoinciden, listaOffsetsSourceFinal)
        listaResultadoHiperonimo = busquedaPalabrasQueSonHiperonimos(palabrasQueCoinciden, listaOffsetsTargetFinal)

        return listaResultadoHiponimo, listaResultadoHiperonimo





########################################################################################################################################################

##################      Método que busca las palabras que son hipónimos y que se mostrarán por pantalla a partir de los offsets que hacen match  ##################

########################################################################################################################################################
def busquedaPalabrasQueSonHiponimos(palabrasQueCoinciden, listaOffsetsSourceFinal):

    resultadoHiponimo = set()
    listaResultadoHiponimo = []
    contadorHipo = 0

    for i in range(len(listaOffsetsSourceFinal)):
        queryResultadoHipo = WeiSpa30Variant.objects.filter(offset=listaOffsetsSourceFinal[i])

        for indiceLista1 in queryResultadoHipo.values():
            if palabrasQueCoinciden[0].word != indiceLista1['word']:
                resultadoHiponimo.add(indiceLista1['word'])
            # print(resultadoHiponimo)

        insertar = resultadoHiponimo.copy()
        listaResultadoHiponimo.insert(contadorHipo, insertar)
        contadorHipo = contadorHipo + 1
        resultadoHiponimo.clear()

    return listaResultadoHiponimo







########################################################################################################################################################

##################      Método que busca las palabras que son hiperónimos y que se mostrarán por pantalla a partir de los offsets que hacen match  ##################

########################################################################################################################################################

def busquedaPalabrasQueSonHiperonimos(palabrasQueCoinciden, listaOffsetsTargetFinal):
    resultadoHiperonimo = set()
    listaResultadoHiperonimo = []
    contadorHiper = 0

    for i in range(len(listaOffsetsTargetFinal)):
        queryResultadoHiper = WeiSpa30Variant.objects.filter(offset=listaOffsetsTargetFinal[i])

        for indiceLista2 in queryResultadoHiper.values():
            if palabrasQueCoinciden[0].word != indiceLista2['word']:
                resultadoHiperonimo.add(indiceLista2['word'])

        insertar = resultadoHiperonimo.copy()
        listaResultadoHiperonimo.insert(contadorHiper, insertar)
        contadorHiper = contadorHiper + 1
        resultadoHiperonimo.clear()

        return listaResultadoHiperonimo



########################################################################################################################################################

##################      Método que busca que sinónimos se encuentran en el archivo de de las 1000 palabras de la RAE  ##################

########################################################################################################################################################

def busquedaSinonimosEnLaRAE(resultadoSinonimos):

    archivo, csvarchivo = aperturaYlecturaCSV()
    listaPalabras = list()

    for fila in range(len(resultadoSinonimos)):
        for palabra in resultadoSinonimos[fila]:
            listaPalabras.append(palabra)
            #print(palabra)


    resultadoListaSinonimosRAE = set()

    for i in range(len(listaPalabras)):
        csvarchivo.seek(0)
        for j in archivo:

            if listaPalabras[i] == j['PALABRA']:
                resultadoListaSinonimosRAE.add(j['PALABRA'])

    return resultadoListaSinonimosRAE




########################################################################################################################################################

##################      Método que busca que hipónimos se encuentran en el archivo de de las 1000 palabras de la RAE  ##################

########################################################################################################################################################

def busquedaHiponimosEnLaRAE(resultadoHiponimo):
    archivo, csvarchivo = aperturaYlecturaCSV()
    listaPalabras = list()

    for fila in range(len(resultadoHiponimo)):
        for palabra in resultadoHiponimo[fila]:
            listaPalabras.append(palabra)
            #print(palabra)


    resultadoListaHiponimosRAE = set()


    for i in range(len(listaPalabras)):
        csvarchivo.seek(0)
        for j in archivo:

            if listaPalabras[i] == j['PALABRA']:
                resultadoListaHiponimosRAE.add(j['PALABRA'])


    return resultadoListaHiponimosRAE




########################################################################################################################################################

##################      Método que busca que hiperónimos se encuentran en el archivo de de las 1000 palabras de la RAE  ##################

########################################################################################################################################################

def busquedaHiperonimosEnLaRAE(resultadoHiperonimo):
    archivo, csvarchivo = aperturaYlecturaCSV()
    listaPalabras = list()

    for fila in range(len(resultadoHiperonimo)):
        for palabra in resultadoHiperonimo[fila]:
            listaPalabras.append(palabra)
            # print(palabra)

    resultadoListaHiperonimosRAE = set()

    for i in range(len(listaPalabras)):
        csvarchivo.seek(0)
        for j in archivo:

            if listaPalabras[i] == j['PALABRA']:
                resultadoListaHiperonimosRAE.add(j['PALABRA'])

    return resultadoListaHiperonimosRAE




def aperturaYlecturaCSV():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    return archivo, csvarchivo
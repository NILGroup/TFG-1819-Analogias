from django.shortcuts import render
from collections import defaultdict
import requests
import csv
import nltk
import os
from nltk.corpus import wordnet as wn
#nltk.download('wordnet');
#nltk.download('omw');




from django.shortcuts import redirect

from .models import WeiSpa30Variant, WeiSpa30Relation
from .forms import PostFormWordSearch




def index(request):
    form = PostFormWordSearch()


    if request.method == "POST":
        form = PostFormWordSearch(request.POST)

        if 'boton-final' in request.POST:

            word = form['word'].value()
            #resultadoSinonimos, resultadoHiponimo, resultadoHiperonimo = #busquedaDePalabras(word)
            #print('resultado' + str(resultadoHiponimo))

            contador, totales = prueba()

            return render(request, 'prototipo/formulario.html', {'form': form, 'contador': contador, 'totales': totales})

    return render(request, 'prototipo/formulario.html', {'form': form })




def prueba():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/prueba.csv', encoding="utf8", errors='ignore')
    entrada = csv.reader(csvarchivo, delimiter=";")
    contador = 0
    totales = 0
    for i in entrada:

        listaResultadoSinonimo, listaResultadoHipo, listaResultadoHiper = busquedaDePalabras(str(i[0]))


        totales = totales + 1

       # print("totales: " + str(totales))
        contador = contador + 1

        #print("encontrados: " + str(contador))

    return contador, totales


def busquedaDePalabras(word):

    #Primero busca que palabras son iguales a la palabra de entrada y nos quedamos con la columna offset
    palabrasQueCoinciden = WeiSpa30Variant.objects.filter(word=word).only('offset')

    #print("SOY unnnnnnn: ")
    #print(len(palabrasQueCoinciden))
    
    #for indice in palabrasQueCoinciden.values():
        #print('palabras que coinciden' + str(indice.values()))

    resultadoSinonimos = busquedadSinonimos(palabrasQueCoinciden)
    #print('sinonimos ' + str(len(resultadoSinonimos)))

    if len(palabrasQueCoinciden) > 0:
        resultadoHiponimo, resultadoHiperonimo = busquedadHipoHiper(palabrasQueCoinciden)

    #print('hiponimos ' + str(len(resultadoHiponimo)))
    #print('hiperonimos ' + str(len(resultadoSinonimos)))

        return resultadoSinonimos, resultadoHiponimo, resultadoHiperonimo
    return -1,-1,-1





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

        resultadoHiponimo = set()
        listaResultadoHiponimo = []
        contadorHipo = 0

        for i in range(len(listaOffsetsSourceFinal)):
            queryResultadoHipo = WeiSpa30Variant.objects.filter(offset=listaOffsetsSourceFinal[i])


            for indiceLista1 in queryResultadoHipo.values():
                resultadoHiponimo.add(indiceLista1['word'])
                #print(resultadoHiponimo)

            insertar = resultadoHiponimo.copy()
            listaResultadoHiponimo.insert(contadorHipo, insertar)
            contadorHipo = contadorHipo + 1
            resultadoHiponimo.clear()

        #print(listaResultadoHiponimo)

        resultadoHiperonimo = set()
        listaResultadoHiperonimo = []
        contadorHiper = 0

        for i in range(len(listaOffsetsTargetFinal)):
            queryResultadoHiper = WeiSpa30Variant.objects.filter(offset=listaOffsetsTargetFinal[i])

            for indiceLista2 in queryResultadoHiper.values():
                resultadoHiperonimo.add(indiceLista2['word'])

            insertar = resultadoHiperonimo.copy()
            listaResultadoHiperonimo.insert(contadorHiper, insertar)
            contadorHiper = contadorHiper + 1
            resultadoHiperonimo.clear()


        return listaResultadoHiponimo, listaResultadoHiperonimo


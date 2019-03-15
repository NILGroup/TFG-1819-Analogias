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

            contadorSinonimos, contadorHiponimos, contadorHiperonimos, totales = prueba()

            return render(request, 'prototipo/formulario.html', {'form': form, 'contadorSinonimos': contadorSinonimos, 'contadorHiponimos': contadorHiponimos, 'contadorHiperonimos': contadorHiperonimos,'totales': totales})

    return render(request, 'prototipo/formulario.html', {'form': form })




def prueba():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/prueba.csv', encoding="utf8", errors='ignore')
    entrada = csv.reader(csvarchivo, delimiter=";")
    contadorSinonimos = 0
    contadorHiponimos = 0
    contadorHiperonimos = 0
    totales = 0

    for i in entrada:

        listaResultadoSinonimo, listaResultadoHipo, listaResultadoHiper = busquedaDePalabras(str(i[0]))

        if len(listaResultadoSinonimo) > 0:
            #print(i[0])
            #print("SINONIMOS:")
            #print(listaResultadoSinonimo)
            #print("HIPONIMOS:")
            #print(listaResultadoHipo)
            #print("HIPERONIMOS:")
            #print(listaResultadoHiper)
            sinonimosRAE = busquedaSinonimosEnLaRAE(listaResultadoSinonimo)
            #print(sinonimosRAE)

            contadorSinonimos = contadorSinonimos + len(sinonimosRAE)
            #print("HIPONIMOS:")
            hiponimosRAE = busquedaHiponimosEnLaRAE(listaResultadoHipo)
            #print(hiponimosRAE)

            contadorHiponimos = contadorHiponimos + len(hiponimosRAE)
            #print("HIPERONIMOS:")
            hiperonimosRAE = busquedaHiperonimosEnLaRAE(listaResultadoHiper)
            #print(hiperonimosRAE)

            contadorHiperonimos = contadorHiperonimos + len(hiperonimosRAE)

        totales = totales + 1



        print("Sinonimos encontrados: " + str(contadorSinonimos) + " de " + str(totales))
        print("Hiponimos encontrados: " + str(contadorHiponimos) + " de " + str(totales))
        print("Hiperonimos encontrados: " + str(contadorHiperonimos) + " de " + str(totales))

        #print("totales: " + str(totales))

    return contadorSinonimos, contadorHiponimos, contadorHiperonimos,totales


def busquedaDePalabras(word):

    #Primero busca que palabras son iguales a la palabra de entrada y nos quedamos con la columna offset
    palabrasQueCoinciden = WeiSpa30Variant.objects.filter(word=word).only('offset')

    #print("SOY unnnnnnn: ")
    #print(len(palabrasQueCoinciden))
    
    #for indice in palabrasQueCoinciden.values():
        #print('palabras que coinciden' + str(indice.values()))

    #DEVUELVE UN SET CON LOS SINONIMOS OBTENIDOS
    resultadoSinonimos = busquedadSinonimos(palabrasQueCoinciden)
    #print('sinonimos ' + str(len(resultadoSinonimos)))


     # DEVUELVE DOS SET UNO CON LOS SINONIMOS OBTENIDOS Y OTRO CON LOS HIPERONIMOS
    resultadoHiponimo, resultadoHiperonimo = busquedadHipoHiper(palabrasQueCoinciden)


    #EL METODO DIFFERENCE ELIMINA LOS ELEMENTOS QUE ESTEN REPETIDOS EN DOS SET Y DEVOLVIENDOLO SIN REPETIDOS
    resultadoSinonimos = resultadoSinonimos.difference(resultadoHiponimo)
    resultadoSinonimos = resultadoSinonimos.difference(resultadoHiperonimo)

    resultadoHiponimo = resultadoHiponimo.difference(resultadoSinonimos)
    resultadoHiponimo = resultadoHiponimo.difference(resultadoHiperonimo)

    resultadoHiperonimo = resultadoHiperonimo.difference(resultadoSinonimos)
    resultadoHiperonimo = resultadoHiperonimo.difference(resultadoHiponimo)




    return resultadoSinonimos, resultadoHiponimo, resultadoHiperonimo






def busquedadSinonimos(palabrasQueCoinciden):

    #set que guarda todos los sinonimos obtenidos de la palabra introducida
    sinonimosPorCadaSynset = set()

    #palabrasQueCoinciden es una lista de offset de cada una de las acepciones de la palabra buscada

    for indiceListaPalabras in range(len(palabrasQueCoinciden)):

        sinonimos = WeiSpa30Variant.objects.filter(offset=palabrasQueCoinciden[indiceListaPalabras].offset)


        for indiceLista in sinonimos.values():
            if palabrasQueCoinciden[0].word != indiceLista['word']:
                sinonimosPorCadaSynset.add(indiceLista['word'])

        #insertar = sinonimosPorCadaSynset.copy()
        #listaResultadoNombres.insert(contador, insertar)
        #contador = contador + 1
        #sinonimosPorCadaSynset.clear()

    return sinonimosPorCadaSynset





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
                if palabrasQueCoinciden[0].word != indiceLista1['word']:
                    resultadoHiponimo.add(indiceLista1['word'])
                #print(resultadoHiponimo)

            #insertar = resultadoHiponimo.copy()
            #listaResultadoHiponimo.insert(contadorHipo, insertar)
            #contadorHipo = contadorHipo + 1
            #resultadoHiponimo.clear()

        #print(listaResultadoHiponimo)

        resultadoHiperonimo = set()
        listaResultadoHiperonimo = []
        contadorHiper = 0

        for i in range(len(listaOffsetsTargetFinal)):
            queryResultadoHiper = WeiSpa30Variant.objects.filter(offset=listaOffsetsTargetFinal[i])

            for indiceLista2 in queryResultadoHiper.values():
                if palabrasQueCoinciden[0].word != indiceLista2['word']:
                    resultadoHiperonimo.add(indiceLista2['word'])

            #insertar = resultadoHiperonimo.copy()
            #listaResultadoHiperonimo.insert(contadorHiper, insertar)
            #contadorHiper = contadorHiper + 1
            #resultadoHiperonimo.clear()


        return resultadoHiponimo, resultadoHiperonimo
    else:
        hiponimosVacios = set()
        hiperonimosVacios = set()
        return hiponimosVacios, hiperonimosVacios


def busquedaSinonimosEnLaRAE(resultadoSinonimos):

    archivo, csvarchivo = aperturaYlecturaCSV()


    resultadoListaSinonimosRAE = set()


    for sinonimo in resultadoSinonimos:

        csvarchivo.seek(0)
        for j in archivo:

            if sinonimo == j['PALABRA']:
                resultadoListaSinonimosRAE.add(j['PALABRA'])



    return resultadoListaSinonimosRAE




def busquedaHiponimosEnLaRAE(resultadoHiponimo):
    archivo, csvarchivo = aperturaYlecturaCSV()


    resultadoListaHiponimosRAE = set()




    for hiponimo in resultadoHiponimo:
        csvarchivo.seek(0)
        for j in archivo:

            if hiponimo == j['PALABRA']:
                resultadoListaHiponimosRAE.add(j['PALABRA'])


    return resultadoListaHiponimosRAE



def busquedaHiperonimosEnLaRAE(resultadoHiperonimo):
    archivo, csvarchivo = aperturaYlecturaCSV()


    resultadoListaHiperonimosRAE = set()

    for hiperonimo in resultadoHiperonimo:
        csvarchivo.seek(0)
        for j in archivo:

            if hiperonimo == j['PALABRA']:
                resultadoListaHiperonimosRAE.add(j['PALABRA'])

    return resultadoListaHiperonimosRAE




def aperturaYlecturaCSV():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    return archivo, csvarchivo



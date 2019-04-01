from django.shortcuts import render
from collections import defaultdict
import requests
import csv
import nltk
import os
from nltk.corpus import wordnet as wn
#nltk.download('wordnet');
#nltk.download('omw');
from .forms import PostForm, PostFormTerminos, PostFormFinal

from django.shortcuts import redirect
from .models import Formulario

# Create your views here.


def index(request):
    form_sinonimos = PostForm()
    form_terminos = PostFormTerminos()
    form_final = PostFormFinal()

    if request.method == "POST":

        #form_final = PostFormFinal(request.POST)


        if 'boton-final' in request.POST:


            contadorSinonimos,contadorTerminos, contadorNoEncontrado,totales = prueba()


            return render(request, 'prototipo/formulario.html', {'contadorSinonimos': contadorSinonimos, 'contadorTerminos': contadorTerminos, 'contadorNoEncontrado': contadorNoEncontrado,'palabrasTotales': totales})

    return render(request, 'prototipo/formulario.html',)



def prueba():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/pruebaFiltrada.csv', encoding="utf8", errors='ignore')
    entrada = csv.reader(csvarchivo, delimiter=";")

    csvSinonimos = open('palabrasConSinonimos.csv', 'w', encoding="utf8", newline="")
    sinonimos = csv.writer(csvSinonimos, delimiter=";")
    sinonimos.writerow(("NUMERO", "SINONIMOS"))

    csvTerminos = open('palabrasConTerminos.csv', 'w', encoding="utf8", newline="")
    terminos = csv.writer(csvTerminos, delimiter=";")
    terminos.writerow(("NUMERO", "TERMINOS"))

    csvNoMatch = open('palabrasSinMatch.csv', 'w', encoding="utf8", newline="")
    sinMatch = csv.writer(csvNoMatch, delimiter=";")
    sinMatch.writerow(("NUMERO", "PALABRA"))

    contadorSinonimos = 0
    contadorTerminos = 0
    contadorNoEncontrado = 0
    totales = 0
    for i in entrada:
        encontradoSinonimos = False
        encontradoTerminos = False
        arraySinonimos, arrayTerminos = busquedaPorNivel(str(i[1]))
        if(len(arraySinonimos) > 0):
            contadorSinonimos = contadorSinonimos + 1
            encontradoSinonimos = True
            sinonimos.writerow((contadorSinonimos, str(i[1])))
        if(len(arrayTerminos) > 0):
            contadorTerminos = contadorTerminos + 1
            encontradoTerminos = True
            terminos.writerow((contadorTerminos, str(i[1])))

        if encontradoSinonimos == False and encontradoTerminos == False:
            contadorNoEncontrado += 1
            sinMatch.writerow((contadorNoEncontrado, str(i[1])))

        totales = totales + 1
        print("Sinonimos encontrados: " + str(contadorSinonimos) + " de " + str(totales))
        print("Terminos encontrados: " + str(contadorTerminos) + " de " + str(totales))
        print("No se han encontrado: " + str(contadorNoEncontrado) + " de " + str(totales))

    csvSinonimos.close()
    csvTerminos.close()
    csvNoMatch.close()
    return contadorSinonimos, contadorTerminos, contadorNoEncontrado, totales - 1




#Dada una palabra, devuelve si hay algún match entre sus terminos relacionados o sinonimos con el csv
def busquedaPorNivel(palabra):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/10000PalabrasFiltradas.csv', encoding="utf8", errors='ignore')
    conjuntoSinonimos = consultaSinonimo(palabra, csvarchivo)
    conjuntoTerminos = consultaTerminos(palabra, csvarchivo)

    return conjuntoSinonimos, conjuntoTerminos




#Servicio Web 3
def consultaSinonimosYterminos(palabra, profundidad):

    #Resultados a pasar al siguiente nivel
    resultadosAcumulados = []
    #Resultados de este nivel
    resultadosActuales = []
    resultadosActualesValidos = []
    encontradoFinal = False

    for contadorProfundidad in range(profundidad):

        contadorProfundidad += 1
        if contadorProfundidad == 1:
            resultadosActuales, encontrado,tipo = busquedaPorNivel(palabra)
            if encontrado == True:
                return resultadosActuales, contadorProfundidad,tipo
        else:
            for i in range(len(resultadosAcumulados)):
                resultados, encontrado, tipo = busquedaPorNivel(resultadosAcumulados[i])
                if encontrado == True:
                    resultadosActualesValidos += resultados
                    encontradoFinal = True
                else:
                    resultadosActuales += resultados

        resultadosAcumulados = resultadosActuales
        if encontradoFinal == True:
            return resultadosActualesValidos, contadorProfundidad,tipo

    if encontradoFinal == False:
        return resultadosActualesValidos, -1, tipo

'''
        if len(arrayconsultaSinonimo) > 0 or len(arrayConsultaTermino) > 0:
            if len(arrayconsultaSinonimo) > 0:
                arrayconsultaSinonimo.append("Se ha encontrado el sinónimo en el nivel de profundidad " + str(contadorProfundidad))
                return arrayconsultaSinonimo
            elif len(arrayConsultaTermino) > 0:
                arrayConsultaTermino.append("Se ha encontrado el término relacionado en el nivel de profundidad " + str(contadorProfundidad))
                return arrayConsultaTermino


    if len(arrayconsultaSinonimo) == 0 and len(arrayConsultaTermino) == 0:
        return "error"

'''



#consulta los sinónimos devueltos de conceptnet con el csv
def consultaSinonimo(palabra, csvarchivo):

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    #devuelve las palabras de conceptnet
    sinonimos = sinonimosDevueltos(palabra)
    conjuntoSinonimos = set()


    for sinonimo in sinonimos:
        csvarchivo.seek(0)
        for j in archivo:

            if sinonimo == j['PALABRA']:
                conjuntoSinonimos.add(j['PALABRA'])



    return conjuntoSinonimos


#Servicio Web 1 que devuelve los sinonimos
def sinonimosDevueltos(palabra):

    conjuntoSalida = set()
    obj = requests.get('http://api.conceptnet.io/c/es/' + palabra + '?offset=0&limit=100').json()
    for j in range(len(obj['edges'])):
        if obj['edges'][j]['rel']['label'] == 'Synonym' and obj['edges'][j]['end']['language'] == 'es' and \
                obj['edges'][j]['start']['label'] == palabra:
            conjuntoSalida.add(obj['edges'][j]['end']['label'])
        elif obj['edges'][j]['rel']['label'] == 'Synonym' and obj['edges'][j]['start']['language'] == 'es' and \
                obj['edges'][j]['end']['label'] == palabra:
            conjuntoSalida.add(obj['edges'][j]['start']['label'])



    return conjuntoSalida



def consultaTerminos(palabra, csvarchivo):

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    terminos = terminosRelacionadosDevueltos(palabra)

    conjuntoTerminos = set()


    for termino in terminos:
        csvarchivo.seek(0)

        for j in archivo:
            if termino == j['PALABRA']:
                conjuntoTerminos.add(j['PALABRA'])

    return conjuntoTerminos



#Servicio Web 2 que devuelve los terminos relacionados
def terminosRelacionadosDevueltos(palabra):

    conjuntoSalida = set()
    obj = requests.get('http://api.conceptnet.io/c/es/' + palabra + '?offset=0&limit=100').json()
    for j in range(len(obj['edges'])):
        if obj['edges'][j]['rel']['label'] == 'RelatedTo' and obj['edges'][j]['end']['language'] == 'es' and \
                obj['edges'][j]['start']['label'] == palabra:
            conjuntoSalida.add(obj['edges'][j]['end']['label'])
        elif obj['edges'][j]['rel']['label'] == 'RelatedTo' and obj['edges'][j]['start']['language'] == 'es' and \
                obj['edges'][j]['end']['label'] == palabra:
            conjuntoSalida.add(obj['edges'][j]['start']['label'])
    return conjuntoSalida
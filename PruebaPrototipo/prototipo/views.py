from django.shortcuts import render
from collections import defaultdict
import requests
import csv
import os

from .forms import PostForm, PostFormTerminos, PostFormFinal

from django.shortcuts import redirect
from .models import Formulario

# Create your views here.


def index(request):
    form_sinonimos = PostForm()
    form_terminos = PostFormTerminos()
    form_final = PostFormFinal()

    if request.method == "POST":
        form_sinonimos = PostForm(request.POST)
        form_terminos = PostFormTerminos(request.POST)
        form_final = PostFormFinal(request.POST)

        if 'boton-sinonimos' in request.POST:
            if form_sinonimos.is_valid():
                form_sinonimos.save()
                resultado = form_sinonimos['campoPalabra'].value()
                salida_sinonimos = sinonimosDevueltos(resultado)
                return render(request, 'prototipo/formulario.html', {'resultadosSinonimos': salida_sinonimos, 'form_term': form_terminos, 'form': form_sinonimos, 'form_final': form_final})

        elif 'boton-terminos' in request.POST:
            if form_terminos.is_valid():
                form_terminos.save()
                resultado = form_terminos['Palabra'].value()
                salida_terminos = terminosRelacionadosDevueltos(resultado)
                return render(request, 'prototipo/formulario.html', {'resultadosTerminos': salida_terminos, 'form_term': form_terminos, 'form': form_sinonimos, 'form_final': form_final})

        elif 'boton-final' in request.POST:
            if form_final.is_valid():
                form_final.save()
                resultado = form_final['Word'].value()
                profundidad = form_final['Depth'].value()
                salida_final = consultaSinonimosYterminos(resultado, profundidad)
                return render(request, 'prototipo/formulario.html', {'form': form_sinonimos, 'form_term': form_terminos, 'resultadosFinal': salida_final, 'form_final': form_final})

    return render(request, 'prototipo/formulario.html', {'form': form_sinonimos, 'form_term': form_terminos, 'form_final': form_final})



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




#Servicio Web 3
def consultaSinonimosYterminos(palabra, profundidad):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')

    arrayconsultaSinonimo = []
    arrayConsultaTermino = []
    contadorProfundidad = 0

    for contadorProfundidad in range(int(profundidad)):

        contadorProfundidad += 1

        if len(arrayconsultaSinonimo) == 0 or len(arrayConsultaTermino) == 0:

            arrayconsultaSinonimo = consultaSinonimo(palabra, csvarchivo)
            if len(arrayconsultaSinonimo) == 0:
                arrayConsultaTermino = consultaTerminos(palabra, csvarchivo)


        if len(arrayconsultaSinonimo) > 0 or len(arrayConsultaTermino) > 0:

            if len(arrayconsultaSinonimo) > 0:
                arrayconsultaSinonimo.append("Se ha encontrado el sinónimo en el nivel de profundidad " + str(contadorProfundidad))
                return arrayconsultaSinonimo
            elif len(arrayConsultaTermino) > 0:
                arrayConsultaTermino.append("Se ha encontrado el término relacionado en el nivel de profundidad " + str(contadorProfundidad))
                return arrayConsultaTermino


    if len(arrayconsultaSinonimo) == 0 and len(arrayConsultaTermino) == 0:
        return "error"





#consulta los sinónimos devueltos de conceptnet con el csv
def consultaSinonimo(palabra, csvarchivo):

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    #devuelve las palabras de conceptnet
    conjuntoContenidoDevuelto = sinonimosDevueltos(palabra)
    listaContenidoDevuelto = list(conjuntoContenidoDevuelto)
    arraySinonimosFinal = []
    encontradoSinonimo = False

    for i in range(len(listaContenidoDevuelto)):
        csvarchivo.seek(0)
        for j in archivo:

            if listaContenidoDevuelto[i] == j['PALABRA']:
                arraySinonimosFinal.append(j['PALABRA'])
                encontradoSinonimo = True


    return arraySinonimosFinal




def consultaTerminos(palabra, csvarchivo):

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    conjuntoContenidoDevuelto = terminosRelacionadosDevueltos(palabra)
    listaContenidoDevuelto = list(conjuntoContenidoDevuelto)
    arrayTerminosFinal = []
    encontradoTermino = False

    for i in range(len(listaContenidoDevuelto)):
        csvarchivo.seek(0)

        for j in archivo:
            if listaContenidoDevuelto[i] == j['PALABRA']:
                arrayTerminosFinal.append(j['PALABRA'])
                encontradoTermino = True

    return arrayTerminosFinal



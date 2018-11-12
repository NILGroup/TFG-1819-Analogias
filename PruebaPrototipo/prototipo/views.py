from django.shortcuts import render
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
                #print(resultado)
                salida_final = consultaSinonimosYterminos(resultado)
               # print(salida_final)
                return render(request, 'prototipo/formulario.html', {'form': form_sinonimos, 'form_term': form_terminos, 'resultadosFinal': salida_final, 'form_final': form_final})

    return render(request, 'prototipo/formulario.html', {'form': form_sinonimos, 'form_term': form_terminos, 'form_final': form_final})



#Servicio Web 1 que devuelve los sinonimos
def sinonimosDevueltos(palabra):

    arraySalida = []
    obj = requests.get('http://api.conceptnet.io/c/es/' + palabra + '?offset=0&limit=100').json()
    for j in range(len(obj['edges'])):
        if obj['edges'][j]['rel']['label'] == 'Synonym' and obj['edges'][j]['end']['language'] == 'es' and \
                obj['edges'][j]['start']['label'] == palabra:
            arraySalida.append("SINONIMO: "+obj['edges'][j]['end']['label'])


    return arraySalida


#Servicio Web 2 que devuelve los terminos relacionados
def terminosRelacionadosDevueltos(palabra):

    arraySalida = []
    obj = requests.get('http://api.conceptnet.io/c/es/' + palabra + '?offset=0&limit=100').json()
    for j in range(len(obj['edges'])):
        if obj['edges'][j]['rel']['label'] == 'RelatedTo' and obj['edges'][j]['end']['language'] == 'es' and \
                obj['edges'][j]['start']['label'] == palabra:
            arraySalida.append("TERMINO RELACIONADO: " + obj['edges'][j]['end']['label'])
    return arraySalida




#Servicio Web 3
def consultaSinonimosYterminos(palabra):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')

    arrayconsultaSinonimo = []
    arrayConsultaTermino = []


    arrayconsultaSinonimo = consultaSinonimo(palabra, csvarchivo)

    if len(arrayconsultaSinonimo) == 0:
        arrayConsultaTermino = consultaTerminos(palabra, csvarchivo)


    if len(arrayconsultaSinonimo) > 0:
        return arrayconsultaSinonimo
    elif len(arrayConsultaTermino) > 0:
        return arrayConsultaTermino




def consultaSinonimo(palabra, csvarchivo):

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    arrayContenidoDevuelto = sinonimosDevueltos(palabra)
    arraySinonimosFinal = []
    encontradoSinonimo = False

    for i in range(len(arrayContenidoDevuelto)):
        csvarchivo.seek(0)
        for j in archivo:
            if encontradoSinonimo == True:
                break
            if arrayContenidoDevuelto[i] == "SINONIMO: " + j['PALABRA']:
                arraySinonimosFinal.append("SINONIMO: " + j['PALABRA'])
                encontradoSinonimo = True


    return arraySinonimosFinal




def consultaTerminos(palabra, csvarchivo):

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    arrayContenidoDevuelto = terminosRelacionadosDevueltos(palabra)
    arrayTerminosFinal = []
    encontradoTermino = False

    for i in range(len(arrayContenidoDevuelto)):
        csvarchivo.seek(0)
        if encontradoTermino == True:
            break
        for j in archivo:
            if arrayContenidoDevuelto[i] == "TERMINO RELACIONADO: " + j['PALABRA']:
                arrayTerminosFinal.append("TERMINO RELACIONADO: " + j['PALABRA'])
                encontradoTermino = True

    return arrayTerminosFinal



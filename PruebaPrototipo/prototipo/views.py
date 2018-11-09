from django.shortcuts import render
import requests
import csv
import os

from .forms import PostForm, PostFormTerminos, PostFormFinal

from django.shortcuts import redirect
from .models import Formulario

# Create your views here.


def index(request):

        if request.method == "POST":
            form_sinonimos = PostForm(request.POST)
            form_terminos = PostFormTerminos(request.POST)
            form_final = PostFormFinal(request.POST)

            if 'boton-sinonimos' in request.POST:
                if form_sinonimos.is_valid():
                    form_sinonimos.save()
                    resultado = form_sinonimos['campoPalabra'].value()
                    salida_sinonimos = sinonimosDevueltos(resultado)
                    return render(request, 'prototipo/formulario.html', {'resultadosSinonimos': salida_sinonimos, 'form_term ': form_terminos, 'form': form_sinonimos})

            elif 'boton-terminos' in request.POST:
                if form_terminos.is_valid():
                    form_terminos.save()
                    resultado = form_terminos['Palabra'].value()
                    salida_terminos = terminosRelacionadosDevueltos(resultado)
                    return render(request, 'prototipo/formulario.html', {'resultadosTerminos': salida_terminos, 'form_term': form_terminos, 'form': form_sinonimos})

            elif 'boton-final' in request.POST:
                if form_final.is_valid():
                    form_final.save()
                    resultado = form_final['Word'].value()
                    #print(resultado)
                    salida_final = consultaSinonimosYterminos(resultado)
                   # print(salida_final)
                    return render(request, 'prototipo/formulario.html', {'resultadosFinal': salida_final, 'form_final': form_final})
        else:
            form_sinonimos = PostForm()
            form_term = PostFormTerminos()
            form_final = PostFormFinal()


        return render(request, 'prototipo/formulario.html', {'form': form_sinonimos, 'form_term': form_term, 'form_final' : form_final})



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


    arrayContenidoDevuelto = []
    arrayContenidoDevuelto = sinonimosDevueltos(palabra)

    arraySinonimosFinal = []
    encontrado = False
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')
    archivo = csv.DictReader(csvarchivo, delimiter=";")


    for i in range(len(arrayContenidoDevuelto)):
        for j in archivo:
            if arrayContenidoDevuelto[i] == "SINONIMO: "+j['PALABRA']:
                arraySinonimosFinal.append(j['PALABRA'])
                encontrado = True


    print(arraySinonimosFinal)
    return arraySinonimosFinal





'''
def sinonimosPalabrasRAE():
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #csvarchivo = open('/Users/IRENE/git/TFG-1819-Analogias/PruebaPrototipo/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')
    #csvarchivo = open('C:/Users/Pablo/Documents/GitHub/TFG-1819-Analogias/PruebaPrototipo/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')
    csvarchivo = open(BASE_DIR+'/prototipo/entrada1000palabrasAPI.csv',encoding="utf8", errors='ignore')
    entrada = csv.DictReader(csvarchivo, delimiter=";")
    arraySalida = []
    for i in entrada:
        obj = requests.get('http://api.conceptnet.io/c/es/' + i['PALABRA'] + '?offset=0&limit=100').json()
        for j in range(len(obj['edges'])):
            if obj['edges'][j]['rel']['label'] == 'Synonym' and obj['edges'][j]['end']['language'] == 'es' and \
                    obj['edges'][j]['start']['label'] == i['PALABRA']:
                arraySalida.append( "Palabra a buscar:" + i['PALABRA'] + "SINONIMO:" + obj['edges'][j]['end']['label'])
            elif obj['edges'][j]['rel']['label'] == 'RelatedTo' and obj['edges'][j]['end']['language'] == 'es' and \
                    obj['edges'][j]['start']['label'] == i['PALABRA']:
                arraySalida.append("Palabra a buscar:" + i['PALABRA'] + "TÉRMINO RELACIONADO:" + obj['edges'][j]['end']['label'])

    csvarchivo.close()
    return arraySalida
'''
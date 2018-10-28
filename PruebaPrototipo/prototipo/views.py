from django.shortcuts import render
import requests
import csv

from .forms import PostForm

from django.shortcuts import redirect
from .models import Formulario

# Create your views here.


def index(request):

        if request.method == "POST":
            if 'boton-principal' in request.POST:
                form = PostForm(request.POST)

                if form.is_valid():
                    form.save()
                    resultado = form['campoPalabra'].value()
                    salida = sinonimosDevueltos(resultado)
                    return render(request, 'prototipo/formulario.html', {'resultados': salida,'form': form})

            elif 'boton-RAE' in request.POST:
                todosSinonimos = sinonimosPalabrasRAE()
                return render(request, 'prototipo/formulario.html', {'todosSinonimos' : todosSinonimos})

        else:
            form = PostForm()

        return render(request, 'prototipo/formulario.html', {'form': form})







def sinonimosDevueltos(palabra):
    arraySalida = []
    obj = requests.get('http://api.conceptnet.io/c/es/' + palabra + '?offset=0&limit=100').json()
    for j in range(len(obj['edges'])):
        if obj['edges'][j]['rel']['label'] == 'Synonym' and obj['edges'][j]['end']['language'] == 'es' and \
                obj['edges'][j]['start']['label'] == palabra:
            arraySalida.append("SINONIMO: "+obj['edges'][j]['end']['label'])

        elif obj['edges'][j]['rel']['label'] == 'RelatedTo' and obj['edges'][j]['end']['language'] == 'es' and \
                obj['edges'][j]['start']['label'] == palabra:
            arraySalida.append("TERMINO RELACIONADO: "+obj['edges'][j]['end']['label'])
    return arraySalida



def sinonimosPalabrasRAE():

    csvarchivo = open('/Users/IRENE/git/TFG-1819-Analogias/PruebaPrototipo/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')
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

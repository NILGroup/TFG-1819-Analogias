from django.shortcuts import render
import requests

from .forms import PostForm
from django.shortcuts import redirect
from .models import Formulario
from django.http import HttpResponseRedirect
# Create your views here.


def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()

            resultado = form['campoPalabra'].value()

            salida = sinonimosDevueltos(resultado)
            return render(request, 'prototipo/formulario.html', {'resultados': salida,'form': form})
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
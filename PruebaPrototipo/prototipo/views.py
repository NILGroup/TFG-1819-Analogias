from django.shortcuts import render
from collections import defaultdict
import requests
import csv
import nltk
import os
from nltk.corpus import wordnet as wn
nltk.download('wordnet');
nltk.download('omw');




from django.shortcuts import redirect

from .models import WeiSpa30Variant, WeiSpa30Relation
from .forms import PostFormWordSearch




def index(request):
    form = PostFormWordSearch()


    if request.method == "POST":
        form = PostFormWordSearch(request.POST)

        if 'boton-final' in request.POST:

            word = form['word'].value()
            resultado = busquedaDePalabras(word)



            return render(request, 'prototipo/formulario.html', {'form': form, 'resultado' : resultado})

    return render(request, 'prototipo/formulario.html', {'form': form })




def busquedaDePalabras(word):

    #Primero busca que palabras son iguales a la palabra de entrada y nos quedamos con la columna offset
    palabrasQueCoinciden = list(WeiSpa30Variant.objects.filter(word=word).only('offset'))



    if len(palabrasQueCoinciden) > 0:
        for indice in range(len(palabrasQueCoinciden)):

            offsetQueEstaEnSourceSynset = list(WeiSpa30Relation.objects.filter(sourcesynset=palabrasQueCoinciden[indice].offset, relation=12).only('relation'))
            print(len(offsetQueEstaEnSourceSynset))

            offsetQueEstaEnTargetSynset = list(WeiSpa30Relation.objects.filter(targetsynset=palabrasQueCoinciden[indice].offset, relation=12).only('relation'))


    return palabrasQueCoinciden


# Create your views here.

'''
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
                return render(request, 'prototipo/formulario.html', {'resultadosSinonimos': salida_sinonimos, 'form_term': form_terminos, 'form': form_sinonimos, 'form_final': form_final, 'encontrado': True})

        elif 'boton-terminos' in request.POST:
            if form_terminos.is_valid():
                form_terminos.save()
                resultado = form_terminos['Palabra'].value()
                salida_terminos = terminosRelacionadosDevueltos(resultado)
                return render(request, 'prototipo/formulario.html', {'resultadosTerminos': salida_terminos, 'form_term': form_terminos, 'form': form_sinonimos, 'form_final': form_final, 'encontrado': True})

        elif 'boton-final' in request.POST:
            if form_final.is_valid():
                form_final.save()
                resultado = form_final['PalabraABuscar'].value()
                profundidad = form_final['Profundidad'].value()
                salida_final, contadorProfundidad, tipo = consultaSinonimosYterminos(resultado, int(profundidad))

                if contadorProfundidad == -1:
                    encontrado = False
                else:
                    encontrado = True
                profundidad = contadorProfundidad
                return render(request, 'prototipo/formulario.html', {'form': form_sinonimos, 'form_term': form_terminos, 'resultadosFinal': salida_final, 'form_final': form_final, 'encontrado': encontrado, 'profundidad': profundidad,'palabraInicial':resultado, 'tipo':tipo})

    return render(request, 'prototipo/formulario.html', {'form': form_sinonimos, 'form_term': form_terminos, 'form_final': form_final, })





#Dada una palabra, devuelve si hay algún match entre sus terminos relacionados o sinonimos con el csv
def busquedaPorNivel(palabra):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')
    arrayconsultaSinonimo, encontrado = consultaSinonimo(palabra, csvarchivo)

    if encontrado == False:
        arrayConsultaTermino, encontrado = consultaTerminos(palabra, csvarchivo)
        if encontrado == False:
            return arrayconsultaSinonimo + arrayConsultaTermino, False," "
        else:
            return arrayConsultaTermino, True,"TERMINO"
    else:
        return arrayconsultaSinonimo, True,"SINONIMO"




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


''' 
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


    if encontradoSinonimo == False:
        return listaContenidoDevuelto, False
    else:
        return arraySinonimosFinal, True


#Servicio Web 1 que devuelve los sinonimos
def sinonimosDevueltos(palabra):
    #http://multiwordnet.fbk.eu/online/mwn-card.php?word=tarantula&language=spanish&id=5144147217&code=11165f88bd2f30d038ded0d3784934d5
    #http://multiwordnet.fbk.eu/online/multiwordnet.php
    #http://www.talp.upc.edu/project-detail/477/EUROWORDNET%20
    #http://multiwordnet.fbk.eu/online/mwn-main.php?language=spanish&field=word&word=tarantula&wntype=Hypernyms&pos=
    #view-source:http://multiwordnet.fbk.eu/online/mwn-main.php?language=spanish&field=word&word=tarantula
    #http://www.talp.upc.edu/
    #http://www.talp.upc.edu/content/multilingual-central-repository-mrc
    #http://www.talp.upc.edu/content/spanish-and-catalan-wordnets-0
    conjuntoSalida = set()
    #conjuntoSalida = []
    lista = wn.synsets(palabra, lang='spa');
   # obj = requests.get('http://multiwordnet.fbk.eu/online/mwn-main.php?language=spanish&field=word&word=tarantula&wntype=Hypernyms&pos=').json()
    #print('resultados api')
    #print(obj)
    """obj = requests.get('http://api.conceptnet.io/c/es/' + palabra + '?offset=0&limit=100').json()
    for j in range(len(obj['edges'])):
        if obj['edges'][j]['rel']['label'] == 'Synonym' and obj['edges'][j]['end']['language'] == 'es' and \
                obj['edges'][j]['start']['label'] == palabra:
            conjuntoSalida.add(obj['edges'][j]['end']['label'])
        elif obj['edges'][j]['rel']['label'] == 'Synonym' and obj['edges'][j]['start']['language'] == 'es' and \
                obj['edges'][j]['end']['label'] == palabra:
            conjuntoSalida.add(obj['edges'][j]['start']['label'])"""

    for i in range(len(lista)):
        for j in range(len(lista[i].lemma_names('spa'))):
            conjuntoSalida.add(lista[i].lemma_names('spa')[j])
            #conjuntoSalida.append(lista[i].lemma_names('spa'))

        #print(lista[i].lemma_names('spa'))



    return conjuntoSalida



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

    if encontradoTermino == False:
        return listaContenidoDevuelto, False
    else:
        return arrayTerminosFinal, True



#Servicio Web 2 que devuelve los terminos relacionados
def terminosRelacionadosDevueltos(palabra):

    lista = wn.synsets(palabra, lang='spa');
    conjuntoSalida = set()
    print('LISTA:')
    print(len(lista))

    for i in range(len(lista)):
        listaHiper = lista[i].hypernyms()
        print("cantidad hiper")
        print(listaHiper)
        for j in range(len(listaHiper)):
            print(listaHiper[j].lemma_names())
        listaHipo = lista[i].hyponyms()
        print("cantidad hipo")
        print(listaHipo)
        for j in range(len(listaHiper)):
            #este if y el de mas abajo son para que no meta vacios en la lista
            if (len(listaHiper[j].lemma_names('spa'))) > 0:
                print('HIPERONIMOS')
                print(listaHiper[j].lemma_names('spa'))
                for k in range(len(listaHiper[j].lemma_names('spa'))):
                    conjuntoSalida.add(listaHiper[j].lemma_names('spa')[k])
                #conjuntoSalida.append(listaHiper[j].lemma_names('spa'))
        for j in range(len(listaHipo)):
            if (len(listaHipo[j].lemma_names('spa'))) > 0:
                print('HIPONIMOS')
                print(listaHipo[j].lemma_names('spa'))
                for k in range(len(listaHipo[j].lemma_names('spa'))):
                    conjuntoSalida.add(listaHipo[j].lemma_names('spa')[k])
                #conjuntoSalida.append(listaHipo[j].lemma_names('spa'))

    return conjuntoSalida

'''
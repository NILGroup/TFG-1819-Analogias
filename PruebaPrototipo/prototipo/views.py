from django.shortcuts import render
import prototipo.functions as f
import prototipo.servicesSearchWords as services
import prototipo.resultsServices as result
import prototipo.spacyService as sp
import prototipo.pictosServices as pictos
import json
import itertools
import functools
import prototipo.customService as custom
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
import base64
from django.db import connection
import os
from .forms import PostFormWordSearch
import shutil



@csrf_exempt
def index(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.exists('prototipo/pictogramas'):
        shutil.rmtree(BASE_DIR + '/prototipo/pictogramas')
    form = PostFormWordSearch()

    if request.method == "POST":
        form = PostFormWordSearch(request.POST)
        if 'button-search' in request.POST:
            word = request.POST.get('word')
            #word = form['word'].value()
            if word.isupper():
                word = word.lower()

            level = request.POST.get('level')
            print("NIVEL")
            print(level)

            allOffset = result.allOffsets(word)
            metaphor = result.getMetaphor(word, level)
            simil = result.getSimil(word, level)


            return JsonResponse({'word' : word, 'allOffsets' : allOffset, 'metaphor' : metaphor, 'simil' : simil})



    return render(request, 'prototipo/aprende_facil.html', {'form': form, 'word': "", 'results': ""})











@csrf_exempt
def version1(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if os.path.exists('prototipo/pictogramas'):
        shutil.rmtree(BASE_DIR + '/prototipo/pictogramas')
    form = PostFormWordSearch()

    if request.method == "POST":
        form = PostFormWordSearch(request.POST)
        if 'button-search' in request.POST:
            word = request.POST.get('word')


            #word = form['word'].value()
            if word.isupper():
                word = word.lower()


            allOffsets = services.allOffsets(word)
            resultsHyperonyms = list()
            resultsSynonyms = list()
            resultsHyponyms = list()

            # resultPictos = list()
            #jsonImage = pictos.getSynsetsAPI(word)


            for offset in allOffsets:
                resultsSynonyms += services.makerSynonymsPhrase(word, offset['offset'])
                resultsHyponyms += services.makerHyponymsPhrase(word, offset['offset'])
                resultsHyperonyms += services.makerHyperonymsPhrase(word, offset['offset'])


            return JsonResponse({'word' : word, 'allOffsets' : allOffsets, 'resultsSynonyms' : resultsSynonyms, 'resultsHyponyms' : resultsHyponyms, 'resultsHyperonyms' : resultsHyperonyms})



    return render(request, 'prototipo/version1.html', {'form': form, 'word': "", 'results': ""})









def version2(request):
    form = PostFormWordSearch()
    #custom.loadIndex()
    if request.method == "POST":
        form = PostFormWordSearch(request.POST)

        if 'button-search' in request.POST:
            # words = request.POST.get('word')
            # print(words)
            word = form['word'].value()
            if word.isupper():
                word = word.lower()
            # print(word)
            # results = services.searchAllHyponyms(word)
            allOffsets = services.allOffsets(word)
            # resultsHyperonyms = list()
            resultsSynonyms = list()
            # resultsHyponyms = list()

            # resultPictos = list()

            jsonImage = pictos.getSynsetsAPI(word)
            fichas = list()

            for offset in allOffsets:
                ficha = ({'picto': "", 'data': []})
                # ficha.append({'picto': "", 'data': []})
                resultsSynonyms = services.makerSynonymsPhrase(word, offset['offset'])
                #resultsSynonyms = custom.customSynonyms(word, offset['offset'], jsonImage)
                resultsHyponyms = services.makerHyponymsPhrase(word, offset['offset'])
                resultsHyperonyms = services.makerHyperonymsPhrase(word, offset['offset'])
                #resultsHyponyms = custom.customHyponyms(word, offset['offset'], jsonImage)
                #resultsHyperonyms = custom.customHyperonyms(word, offset['offset'], jsonImage)

                if len(resultsSynonyms) > 0:
                    elem = ({'tipo': "", 'datos': ""})
                    # elem.append({'tipo': "", 'datos': ""})
                    elem['tipo'] = 'synonyms'
                    elem['datos'] = resultsSynonyms[0]
                    ficha['data'].append(elem)
                if len(resultsHyponyms) > 0:
                    elem = ({'tipo': "", 'datos': ""})
                    # elem.append({'tipo': "", 'datos': ""})
                    elem['tipo'] = 'hyponyms'
                    elem['datos'] = resultsHyponyms
                    # print(resultsHyponyms)
                    ficha['data'].append(elem)
                if len(resultsHyperonyms) > 0:
                    elem = ({'tipo': "", 'datos': ""})
                    # elem.append({'tipo': "", 'datos': ""})
                    elem['tipo'] = 'hyperonyms'
                    elem['datos'] = resultsHyperonyms
                    ficha['data'].append(elem)
                if len(resultsSynonyms) > 0 or len(resultsHyponyms) > 0 or len(resultsHyperonyms) > 0:

                    #start_time = time.time()
                    #url = pictos.getImage(offset['offset'], jsonImage)
                    with connection.cursor() as cursor:

                        cursor.execute('SELECT id_picto FROM pictos WHERE offset30 = %s', [offset['offset']])
                        rows = cursor.fetchall()
                        #print(len(rows))
                        if len(rows) > 0:


                            url = 'https://api.arasaac.org/api/pictograms/'+str(rows[0][0]) +'?download=false'
                    #print(time.time() - start_time)

                            ficha['picto'] = url

                    fichas.append(ficha)
                '''
                for synsets in resultPictos:
                    print(offset['offset'])
                    print(synsets["synsets"])
                    #url = pictos.getImage(offset['offset'], synsets)
                    #print(url)
                    '''

            # print("HYPERONYMS")
            # print(resultsHyperonyms)
            # print("HYPONYMS")
            # print(resultsHyponyms)
            # print("SYNONYMS")
            #print(resultsSynonyms)
            print(fichas)
            '''
            if len(resultsHyperonyms) > 0:
                for elem in resultsHyperonyms:
                    #print(elem['offsetFather'])
                    url = pictos.getImage(str(elem['offsetFather']), jsonPictos)
                    if url != "None":
                        elem['picto'] = url
            '''

            return render(request, 'prototipo/version2.html',
                          {'form': form, 'word': word, 'counter': functools.partial(next, itertools.count(1)),
                           'counterId': functools.partial(next, itertools.count(1)), 'fichas': fichas})

    return render(request, 'prototipo/version2.html', {'form': form, 'word': "", 'results': ""})







def prueba(request):
    form = PostFormWordSearch()

    if request.method == "POST":
        form = PostFormWordSearch(request.POST)

        if 'boton-final' in request.POST:

            word = form['word'].value()
            resultadoSinonimos , resultadoHiponimo, resultadoHiperonimo  = f.busquedaDePalabras(word)

            profundidad = 1
            encontrado = False

            dict_resultados = dict(sinonimos="", hiponimos="", hiperonimos="")

            while profundidad <= 3 and encontrado == False:
                dict_resultados["sinonimos"] = list(f.busquedaSinonimosEnLaRAE(resultadoSinonimos, profundidad))
                dict_resultados["hiponimos"] = list(f.busquedaHiponimosEnLaRAE(resultadoHiponimo, profundidad))
                dict_resultados["hiperonimos"] = list(f.busquedaHiperonimosEnLaRAE(resultadoHiperonimo, profundidad))

                if len(dict_resultados["sinonimos"]) > 0 or len(dict_resultados["hiponimos"]) > 0 or len(
                        dict_resultados["hiperonimos"]) > 0:
                    encontrado = True

                profundidad += 1

            return render(request, 'prototipo/formulario.html', {'form': form, 'resultadoSinonimos': resultadoSinonimos,
                                                                 'resultadoHiponimo': resultadoHiponimo,
                                                                 'resultadoHiperonimo': resultadoHiperonimo,
                                                                 'word': word, 'dict': dict_resultados,
                                                                 'json': json.dumps(dict_resultados,
                                                                                ensure_ascii=False)})

    return render(request, 'prototipo/formulario.html', {'form': form})


def getImagen(request, offset):

    if not os.path.exists('prototipo/pictogramas'):
        os.makedirs('prototipo/pictogramas', mode=0o777)
    with connection.cursor() as cursor:
        cursor.execute('SELECT imagen FROM pictos WHERE offset30 = %s', [offset])
        rows = cursor.fetchall()
        #print(len(rows))
        if len(rows) > 0:
            image_64_decode = base64.decodebytes(rows[0][0])
            image_result = open('prototipo/pictogramas/'+offset+'.png', 'wb')
            image_result.write(image_64_decode)
            image_result.close()
            imagen = open('prototipo/pictogramas/'+offset+'.png', 'rb').read()

            return HttpResponse(imagen, content_type="image/png")

    notFound = ['pictograma no encontrado']
    return JsonResponse(notFound, safe=False)


def getImagenPalabra(request, palabra):

    if not os.path.exists('prototipo/pictogramas'):
        os.makedirs('prototipo/pictogramas', mode=0o777)
    with connection.cursor() as cursor:
        cursor.execute('SELECT imagen FROM pictos WHERE palabra = %s', [palabra])
        rows = cursor.fetchall()
        #print(len(rows))
        if len(rows) > 0:
            image_64_decode = base64.decodebytes(rows[0][0])
            image_result = open('prototipo/pictogramas/'+palabra+'.png', 'wb')
            image_result.write(image_64_decode)
            image_result.close()
            imagen = open('prototipo/pictogramas/'+palabra+'.png', 'rb').read()

            return HttpResponse(imagen, content_type="image/png")
    notFound = ['pictograma no encontrado']
    return JsonResponse(notFound, safe=False)

'''
def index(request):
    form = PostFormWordSearch()

    if request.method == "POST":
        form = PostFormWordSearch(request.POST)

        if 'button-search' in request.POST:
            # words = request.POST.get('word')
            # print(words)
            word = form['word'].value()
            # print(word)
            # results = services.searchAllHyponyms(word)
            allOffsets = services.allOffsets(word)
            # resultsHyperonyms = list()
            # resultsSynonyms = list()
            # resultsHyponyms = list()

            # resultPictos = list()
            jsonImage = pictos.getSynsetsAPI(word)
            fichas = list()

            for offset in allOffsets:
                ficha = ({'picto': "", 'data': []})
                # ficha.append({'picto': "", 'data': []})
                # resultsSynonyms += services.makerSynonymsPhrase(word, offset['offset'])
                resultsSynonyms = services.customSynonyms(word, offset['offset'], jsonImage)
                resultsHyponyms = services.customHyponyms(word, offset['offset'], jsonImage)
                resultsHyperonyms = services.customHyperonyms(word, offset['offset'], jsonImage)

                if len(resultsSynonyms) > 0:
                    elem = ({'tipo': "", 'datos': ""})
                    # elem.append({'tipo': "", 'datos': ""})
                    elem['tipo'] = 'synonyms'
                    elem['datos'] = resultsSynonyms[0]
                    ficha['data'].append(elem)
                if len(resultsHyponyms) > 0:
                    elem = ({'tipo': "", 'datos': ""})
                    # elem.append({'tipo': "", 'datos': ""})
                    elem['tipo'] = 'hyponyms'
                    elem['datos'] = resultsHyponyms
                    # print(resultsHyponyms)
                    ficha['data'].append(elem)
                if len(resultsHyperonyms) > 0:
                    elem = ({'tipo': "", 'datos': ""})
                    # elem.append({'tipo': "", 'datos': ""})
                    elem['tipo'] = 'hyperonyms'
                    elem['datos'] = resultsHyperonyms
                    ficha['data'].append(elem)
                if len(resultsSynonyms) > 0 or len(resultsHyponyms) > 0 or len(resultsHyperonyms) > 0:
                    url = pictos.getImage(offset['offset'], jsonImage)
                    if url != "None":
                        ficha['picto'] = url

                    fichas.append(ficha)

            if len(resultsHyperonyms) > 0:
                for elem in resultsHyperonyms:
                    # print(elem['offsetFather'])
                    url = pictos.getImage(str(elem['offsetFather']), jsonPictos)
                    if url != "None":
                        elem['picto'] = url

            return render(request, 'prototipo/index.html',
                          {'form': form, 'word': word, 'counter': functools.partial(next, itertools.count(1)),
                           'counterId': functools.partial(next, itertools.count(1)), 'fichas': fichas})

    return render(request, 'prototipo/index.html', {'form': form, 'word': "", 'results': ""})
'''
##### -------   SERVICIOS PARA PETICIONES GET MEDIANTE URL -------######



def getSynonymsJsonResults(request, word, level):

    easySynonym = result.getEasySynonyms(word, level)

    return HttpResponse(easySynonym,
                 content_type="application/json")


def getHyponymsJsonResults(request, word, level):
    easyHyponym = result.getEasyHyponyms(word, level)

    return HttpResponse(json.dumps(easyHyponym, ensure_ascii=False),
                        content_type="application/json")


def getHyperonymsJsonResults(request, word, level):
    easyHyperonym = result.getEasyHyperonyms(word, level)

    return HttpResponse(json.dumps(easyHyperonym, ensure_ascii=False),
                        content_type="application/json")


def getMetaphor(request, word, level):

    methapor = result.getMetaphor(word, level)

    return HttpResponse(json.dumps(methapor, ensure_ascii=False),
                        content_type="application/json")


def getSimil(request, word, level):

    methapor = result.getSimil(word, level)

    return HttpResponse(json.dumps(methapor, ensure_ascii=False),
                        content_type="application/json")


def getDefAndExample(request, word, level):

    content = result.getDefAndExample(word, level)

    return HttpResponse(json.dumps(content, ensure_ascii=False),
                        content_type="application/json")
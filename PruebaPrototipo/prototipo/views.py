from django.shortcuts import render
import prototipo.functions as f
import prototipo.servicesSearchWords as services
import prototipo.spacyService as sp
import prototipo.pictosServices as pictos
import json
import itertools
import functools
import prototipo.customService as custom
import time


from .forms import PostFormWordSearch


def index(request):
    form = PostFormWordSearch()

    if request.method == "POST":
        form = PostFormWordSearch(request.POST)

        if 'button-search' in request.POST:
           # words = request.POST.get('word')
            #print(words)
            word = form['word'].value()
            #print(word)
            #results = services.searchAllHyponyms(word)
            allOffsets = services.allOffsets(word)
            #resultsHyperonyms = list()
            #resultsSynonyms = list()
            #resultsHyponyms = list()

            #resultPictos = list()
            jsonImage = pictos.getSynsetsAPI(word)
            fichas = list()

            for offset in allOffsets:
                ficha = ({'picto': "", 'data': []})
                #ficha.append({'picto': "", 'data': []})
                #resultsSynonyms += services.makerSynonymsPhrase(word, offset['offset'])
                resultsSynonyms = services.customSynonyms(word, offset['offset'], jsonImage)
                resultsHyponyms = services.customHyponyms(word, offset['offset'], jsonImage)
                resultsHyperonyms = services.customHyperonyms(word, offset['offset'], jsonImage)

                if len(resultsSynonyms) > 0:
                    elem = ({'tipo': "", 'datos': ""})
                    #elem.append({'tipo': "", 'datos': ""})
                    elem['tipo'] = 'synonyms'
                    elem['datos'] = resultsSynonyms[0]
                    ficha['data'].append(elem)
                if len(resultsHyponyms) > 0:
                    elem = ({'tipo': "", 'datos': ""})
                    #elem.append({'tipo': "", 'datos': ""})
                    elem['tipo'] = 'hyponyms'
                    elem['datos'] = resultsHyponyms
                    #print(resultsHyponyms)
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
                '''
                for synsets in resultPictos:
                    print(offset['offset'])
                    print(synsets["synsets"])
                    #url = pictos.getImage(offset['offset'], synsets)
                    #print(url)
                    '''

            #print("HYPERONYMS")
            #print(resultsHyperonyms)
            #print("HYPONYMS")
            #print(resultsHyponyms)
            #print("SYNONYMS")
            #print(resultsSynonyms)
            #print(fichas)
            '''
            if len(resultsHyperonyms) > 0:
                for elem in resultsHyperonyms:
                    #print(elem['offsetFather'])
                    url = pictos.getImage(str(elem['offsetFather']), jsonPictos)
                    if url != "None":
                        elem['picto'] = url
            '''

            return render(request, 'prototipo/index.html', {'form': form, 'word': word, 'counter' :functools.partial(next, itertools.count(1)), 'counterId' :functools.partial(next, itertools.count(1)),'fichas': fichas})



    return render(request, 'prototipo/index.html', {'form': form, 'word': "", 'results': ""})



def version1(request):

    form = PostFormWordSearch()

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
            resultsHyperonyms = list()
            resultsSynonyms = list()
            resultsHyponyms = list()

            # resultPictos = list()
            jsonImage = pictos.getSynsetsAPI(word)
            fichas = list()

            for offset in allOffsets:

                resultsSynonyms += services.makerSynonymsPhrase(word, offset['offset'])
                resultsHyponyms += services.makerHyponymsPhrase(word, offset['offset'])
                resultsHyperonyms += services.makerHyperonymsPhrase(word, offset['offset'])



            return render(request, 'prototipo/version1.html',
                          {'form': form, 'word': word, 'counter': functools.partial(next, itertools.count(1)),
                           'counterId': functools.partial(next, itertools.count(1)), 'offsetInicial' : allOffsets, 'resultsSynonyms': resultsSynonyms, 'resultsHyponyms' : resultsHyponyms, 'resultsHyperonyms' : resultsHyperonyms})

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
            # resultsSynonyms = list()
            # resultsHyponyms = list()

            # resultPictos = list()

            jsonImage = pictos.getSynsetsAPI(word)
            fichas = list()

            for offset in allOffsets:
                ficha = ({'picto': "", 'data': []})
                # ficha.append({'picto': "", 'data': []})
                # resultsSynonyms += services.makerSynonymsPhrase(word, offset['offset'])
                resultsSynonyms = custom.customSynonyms(word, offset['offset'], jsonImage)
                resultsHyponyms = custom.customHyponyms(word, offset['offset'], jsonImage)
                resultsHyperonyms = custom.customHyperonyms(word, offset['offset'], jsonImage)

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
                    start_time = time.time()
                    url = pictos.getImage(offset['offset'], jsonImage)
                    print('T PICTO')
                    print(time.time() - start_time)
                    if url != "None":
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
            # print(resultsSynonyms)
            # print(fichas)
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




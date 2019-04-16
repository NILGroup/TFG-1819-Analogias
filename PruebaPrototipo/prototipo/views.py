from django.shortcuts import render
import prototipo.functions as f
import prototipo.servicesSearchWords as services
import prototipo.spacyService as sp
import prototipo.pictosServices as pictos
import json
import itertools
import functools



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
            #jsonPictos = pictos.getSynsetsAPI(word)
            fichas = list()

            for offset in allOffsets:
                ficha = list()

                #resultsSynonyms += services.makerSynonymsPhrase(word, offset['offset'])
                resultsSynonyms = services.customSynonyms(word, offset['offset'])
                resultsHyponyms = services.customHyponyms(word, offset['offset'])
                resultsHyperonyms = services.customHyperonyms(word, offset['offset'])
                if len(resultsSynonyms) > 0:
                    elem = []
                    elem.append({'tipo': "", 'datos': ""})
                    elem[0]['tipo'] = 'synonyms'
                    elem[0]['datos'] = resultsSynonyms
                    ficha.append(elem)
                if len(resultsHyponyms) > 0:
                    elem = []
                    elem.append({'tipo': "", 'datos': ""})
                    elem[0]['tipo'] = 'hyponyms'
                    elem[0]['datos'] = resultsHyponyms
                    ficha.append(elem)
                if len(resultsHyperonyms) > 0:
                    elem = []
                    elem.append({'tipo': "", 'datos': ""})
                    elem[0]['tipo'] = 'hyperonyms'
                    elem[0]['datos'] = resultsHyperonyms
                    ficha.append(elem)
                if len(ficha) > 0:
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
            print(len(fichas))
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




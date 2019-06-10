from django.shortcuts import render
import prototipo.resultsServices as result
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse

import os
from .forms import PostFormWordSearch




@csrf_exempt
def principal(request, word, level):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if request.method == "GET":


        allOffset = result.allOffsets(word)
        metaphor = result.getMetaphor(word, level)

        simil = result.getSimil(word, level)
        def_and_example = result.getDefAndExample(word, level)

        return JsonResponse({'word': word, 'allOffsets': allOffset, 'metaphor': metaphor, 'simil': simil,
                                 'content': def_and_example})

    return render(request, 'prototipo/aprende_facil.html', { 'word': "", 'results': ""})





@csrf_exempt
def index(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #if os.path.exists('prototipo/pictogramas'):
        #shutil.rmtree(BASE_DIR + '/prototipo/pictogramas')
    form = PostFormWordSearch()

    if request.method == "POST":
        form = PostFormWordSearch(request.POST)
        if 'button-search' in request.POST:
            word = request.POST.get('word')
            word = word.lower()


            level = request.POST.get('level')


            allOffset = result.allOffsets(word)
            simil = result.getSimil(word, level)
            metaphor = result.getMetaphor(word, level)

            def_and_example = result.getDefAndExample(word, level)


            return JsonResponse({'word' : word, 'allOffsets' : allOffset, 'metaphor' : metaphor, 'simil' : simil, 'content' : def_and_example})



    return render(request, 'prototipo/aprende_facil.html', {'form': form, 'word': "", 'results': ""})







def getImagen(request, offset):

    return result.getImageOffset(offset)


def getImagenPalabra(request, palabra):

    return result.getImagePalabra(palabra)

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
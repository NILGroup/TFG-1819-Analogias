from .models import *
import os

from prototipo import spacyService as spacy

import django

django.setup()
from django.db import connection

import base64

from django.http import JsonResponse
from django.http import HttpResponse
repeatWords = set()

### SERVICIO QUE DADA UNA PALABRA Y UN NIVEL DEVUELVE SUS SINONIMOS FACILES  ###

def getEasySynonyms(word, level):
    global repeatWords
    dataJson = []
    ##  Devuelve todos los offsets de los synsets de dicha palabra
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')
    index = 1
    dataJson.insert(0, {'word': ""})
    dataJson[0]["word"] = word
    tipo, gender, number = spacy.genderAndNumberAPI(word)


    for offset in listOffsetToTheSynset:
        ##   Devuelve todos los sinónimos de esa palabra
        listaSynonyms = WeiSpa30Variant.objects.filter(offset=offset['offset']).values('word').distinct()


        ##   Por cada sinónimo, busca si se encuentra en la base de datos de las palabras fáciles
        listEasyWords = list()
        for synonym in listaSynonyms:
            if synonym['word'] != word:
                with connection.cursor() as cursor:
                    if level == "1":
                        cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s AND tag = %s',
                                               [synonym['word'], tipo])
                    elif level == "2":
                        cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s AND tag = %s',
                                               [synonym['word'], tipo])
                    else:
                        cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s AND tag = %s',
                                               [synonym['word'], tipo])

                    result = cursor.fetchone()[0]
                    if result > 0:
                        if synonym['word'] not in repeatWords:
                            repeatWords.add(synonym['word'])
                            listEasyWords.append(synonym['word'])

        if len(listEasyWords) > 0:
            dataJson.append({'offset': "", 'synonyms': []})
            dataJson[index]['offset'] = offset['offset']
            dataJson[index]['synonyms'] = listEasyWords

            index += 1




    return dataJson


### SERVICIO QUEDADA UNA PALABRA Y UN NIVEL DEVUELVE SUS HIPONIMOS FACILES ###

def getEasyHyponyms(word, level):

    dataJson = []
    ##  Devuelve todos los offsets de los synsets de dicha palabra
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')
    tipo, gender, number = spacy.genderAndNumberAPI(word)
    index = 1
    dataJson.insert(0, {'word': ""})
    dataJson[0]["word"] = word
    global repeatWords

    for offset in listOffsetToTheSynset:
        offsetMatchSourceSynset = (WeiSpa30Relation.objects.filter(sourcesynset=offset['offset'], relation=12)).values(
            'targetsynset').distinct()

        if len(offsetMatchSourceSynset) > 0:
            listEasyWords = list()
            for targetSynset in offsetMatchSourceSynset:
                listaWordsHyponyms = WeiSpa30Variant.objects.filter(offset=targetSynset['targetsynset']).values('word').distinct()

                for hyponym in listaWordsHyponyms:
                    if hyponym['word'] != word:
                        with connection.cursor() as cursor:
                            if level == "1":
                                cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s AND tag = %s',
                                               [hyponym['word'], tipo])
                            elif level == "2":
                                cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s AND tag = %s',
                                               [hyponym['word'], tipo])
                            else:
                                cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s AND tag = %s',
                                               [hyponym['word'], tipo])

                            result = cursor.fetchone()[0]
                            if result > 0:
                                if hyponym['word'] not in repeatWords:
                                    repeatWords.add(hyponym['word'])
                                    listEasyWords.append(hyponym['word'])
            if len(listEasyWords) > 0:
                dataJson.append(
                    {'offsetFather': "", 'offset': "", 'hyponyms': []})
                dataJson[index]["offsetFather"] = offset['offset']
                dataJson[index]["offset"] = targetSynset["targetsynset"]
                dataJson[index]["hyponyms"] = listEasyWords

                index += 1

    return dataJson

### SERVICIO QUE DADA UNA PALABRA Y UN NIVEL DEVUELVE SUS HIPERONIMOS FACILES ###

def getEasyHyperonyms(word, level):
    global repeatWords
    dataJson = []
    ##  Devuelve todos los offsets de los synsets de dicha palabra
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')
    index = 1
    dataJson.insert(0, {'word': ""})
    dataJson[0]["word"] = word
    tipo, gender, number = spacy.genderAndNumberAPI(word)

    for offset in listOffsetToTheSynset:
        offsetMatchTargetSynset = (WeiSpa30Relation.objects.filter(targetsynset=offset['offset'], relation=12)).values(
            'sourcesynset').distinct()

        if len(offsetMatchTargetSynset) > 0:
            listEasyWords = list()
            for sourceSynset in offsetMatchTargetSynset:
                listaWordsHyperonyms = WeiSpa30Variant.objects.filter(offset=sourceSynset['sourcesynset']).values(
                    'word').distinct()

                for hyperonym in listaWordsHyperonyms:
                    if hyperonym['word'] != word:
                        with connection.cursor() as cursor:
                            if level == "1":
                                cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s AND tag = %s',
                                               [hyperonym['word'], tipo])
                            elif level == "2":
                                cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s AND tag = %s',
                                               [hyperonym['word'], tipo])
                            else:
                                cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s AND tag = %s',
                                               [hyperonym['word'], tipo])

                            result = cursor.fetchone()[0]
                            if result > 0:
                                if hyperonym['word'] not in repeatWords:
                                    repeatWords.add(hyperonym['word'])
                                    listEasyWords.append(hyperonym['word'])
            if len(listEasyWords) > 0:
                dataJson.append(
                    {'offsetFather': "", 'offset': "", 'hyperonyms': []})
                dataJson[index]["offsetFather"] = offset['offset']
                dataJson[index]["offset"] = sourceSynset["sourcesynset"]
                dataJson[index]["hyperonyms"] = listEasyWords

                index += 1
    return dataJson


### SERVICIO QUE DADA UNA PALABRA Y UN NIVEL DEVUELVE UNA METÁFORA ###


def getMetaphor(word, level):

    dataJson = []
    global repeatWords

    dataJson.insert(0, {'word': ""})
    dataJson[0]["word"] = word


    listEasySynonymsWords = getEasySynonyms(word, level)

    index = 1
    if len(listEasySynonymsWords) > 1:
        for elem in range(len(listEasySynonymsWords) - 1):
            phraseSynonym = list()
            dataJson.append(
            {'type': "SYNONYM", 'offset': "", 'metaphor': []})
            dataJson[index]['offset'] = listEasySynonymsWords[index]['offset']

            for synonym in listEasySynonymsWords[index]['synonyms']:
                phraseSynonym.append(spacy.phraseMaker(synonym))

            dataJson[index]['metaphor'] = phraseSynonym
            index += 1


    listEasyHyperonymsWords = getEasyHyperonyms(word, level)


    indexHyperonym = 1
    if len(listEasyHyperonymsWords) > 1:
        for elem in range(len(listEasyHyperonymsWords) - 1):
            phraseHyperonym = list()

            dataJson.append(
                {'type' : "HYPERONYM", 'offsetFather': "", 'offset': "", 'metaphor': []})
            dataJson[index]["offsetFather"] = listEasyHyperonymsWords[indexHyperonym]['offsetFather']
            dataJson[index]["offset"] = listEasyHyperonymsWords[indexHyperonym]['offset']
            for hyperonym in listEasyHyperonymsWords[indexHyperonym]['hyperonyms']:
                phraseHyperonym.append(spacy.phraseMaker(hyperonym))

            dataJson[index]['metaphor'] = phraseHyperonym
            index += 1
            indexHyperonym += 1


    if len(dataJson) == 1:
        dataJson.pop()

    repeatWords.clear()
    return dataJson


### SERVICIO QUE DADA UNA PALABRA Y UN NIVEL DEVUELVE UN SIMIL ###


def getSimil(word, level):
    dataJson = []
    global repeatWords
    ##  Devuelve todos los offsets de los synsets de dicha palabra
    index = 1
    dataJson.insert(0, {'word': ""})
    dataJson[0]["word"] = word

    listEasyWords = getEasyHyponyms(word, level)

    if len(listEasyWords) > 1:

        for elem in range(len(listEasyWords) - 1):
            phraseHyponym = list()

            dataJson.append(
                {'offsetFather': "", 'offset': "",
                 'simil': []})
            dataJson[index]["offsetFather"] = listEasyWords[index]['offsetFather']
            dataJson[index]["offset"] = listEasyWords[index]["offset"]
            for hyponym in listEasyWords[index]['hyponyms']:
                phraseHyponym.append(spacy.phraseMakerForHyponyms(hyponym))
            dataJson[index]['simil'] = phraseHyponym
            index += 1


    if len(dataJson) == 1:
        dataJson.pop()
    return dataJson



####    SERVICIO QUE DADA UNA PALABRA DEVUELVE TODOS SUS OFFSETS    ####

 
def getDefAndExample(word, level):
    dataJson = []

    global repeatWords

    dataJson.insert(0, {'word' : ""})
    dataJson.insert(1, {"metaphor" : []})
    dataJson.insert(2, {"simil" : []})
    dataJson[0]["word"] = word

    i_simil = 0
    i_simil_entrada = 1
    i_metaphor = 0
    i_metaphor_entrada = 1

    data_simil = getSimil(word, level)
    if len(data_simil) > 1:

        for elem in range(len(data_simil) - 1):
            definitionHypo = WeiSpa30Synset.objects.filter(offset=data_simil[i_simil_entrada]['offset']).values('gloss')
            exampleHypo = WeiSpa30Examples.objects.filter(offset=data_simil[i_simil_entrada]['offset']).values(
                'examples')
            if definitionHypo[0]["gloss"] != "None" or len(exampleHypo) > 0:
                listExamplesHypo = list()

                dataJson[2]['simil'].append(
                    ({'type': "HYPONYM", 'offsetFather': "", 'offset': "", 'definition': "", 'example': []}))

                dataJson[2]['simil'][i_simil]['offsetFather'] = data_simil[i_simil_entrada]['offsetFather']
                dataJson[2]['simil'][i_simil]['offset'] = data_simil[i_simil_entrada]['offset']

                if definitionHypo[0]["gloss"] != "None":
                    if len(definitionHypo) > 0:
                        dataJson[2]['simil'][i_simil]["definition"] = definitionHypo[0]['gloss']

                if len(exampleHypo) > 0:
                    for example in exampleHypo:
                        listExamplesHypo.append(example['examples'])
                    dataJson[2]['simil'][i_simil]["example"] = listExamplesHypo
                i_simil += 1
            i_simil_entrada += 1

    data_metaphor = getMetaphor(word, level)
    if len(data_metaphor) > 1:
        for elem in range(len(data_metaphor) - 1):
            definitionMeta = WeiSpa30Synset.objects.filter(offset=data_metaphor[i_metaphor_entrada]['offset']).values(
                'gloss')
            exampleMeta = WeiSpa30Examples.objects.filter(offset=data_metaphor[i_metaphor_entrada]['offset']).values(
                'examples')
            if definitionMeta[0]["gloss"] != "None" or len(exampleMeta) > 0:
                listExamplesMeta = list()
                dataJson[1]['metaphor'].append(({'type': "", 'offsetFather': "", 'offset': "", 'definition': "", 'example': []}))
                dataJson[1]['metaphor'][i_metaphor]['offset'] = data_metaphor[i_metaphor_entrada]['offset']
                dataJson[1]['metaphor'][i_metaphor]['type'] = data_metaphor[i_metaphor_entrada]['type']
                if data_metaphor[i_metaphor_entrada]['type'] == "HYPERONYM":
                    dataJson[1]['metaphor'][i_metaphor]['offsetFather'] = data_metaphor[i_metaphor_entrada]['offsetFather']
                if definitionMeta[0]["gloss"] != "None":
                    if len(definitionMeta) > 0:
                        dataJson[1]['metaphor'][i_metaphor]["definition"] = definitionMeta[0]['gloss']

                if len(exampleMeta) > 0:
                    for example in exampleMeta:
                        listExamplesMeta.append(example['examples'])
                    dataJson[1]['metaphor'][i_metaphor]["example"] = listExamplesMeta
                i_metaphor += 1
            i_metaphor_entrada += 1

    repeatWords.clear()

    return dataJson

####    SERVICIO QUE DADA UNA PALABRA DEVUELVE TODOS SUS OFFSETS    ####

def allOffsets(word):
    dataJson = []
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')

    index = 0

    for offset in listOffsetToTheSynset:
        dataJson.insert(index, {'offset': ""})
        dataJson[index]["offset"] = offset['offset']
        index += 1

    return dataJson


def getImagePalabra(palabra):
    if not os.path.exists('prototipo/pictogramas'):
        os.makedirs('prototipo/pictogramas', mode=0o777)
    with connection.cursor() as cursor:
        cursor.execute('SELECT imagen FROM pictos WHERE palabra = %s', [palabra])
        rows = cursor.fetchall()

        if len(rows) > 0:
            image_64_decode = base64.decodebytes(rows[0][0])
            image_result = open('prototipo/pictogramas/'+palabra+'.png', 'wb')
            image_result.write(image_64_decode)
            image_result.close()
            imagen = open('prototipo/pictogramas/'+palabra+'.png', 'rb').read()

            return HttpResponse(imagen, content_type="image/png")
    notFound = ['pictograma no encontrado']
    return JsonResponse(notFound, safe=False)

def getImageOffset(offset):
    if not os.path.exists('prototipo/pictogramas'):
        os.makedirs('prototipo/pictogramas', mode=0o777)
    with connection.cursor() as cursor:
        cursor.execute('SELECT imagen FROM pictos WHERE offset30 = %s', [offset])
        rows = cursor.fetchall()

        if len(rows) > 0:
            image_64_decode = base64.decodebytes(rows[0][0])
            image_result = open('prototipo/pictogramas/'+offset+'.png', 'wb')
            image_result.write(image_64_decode)
            image_result.close()
            imagen = open('prototipo/pictogramas/'+offset+'.png', 'rb').read()

            return HttpResponse(imagen, content_type="image/png")

    notFound = ['pictograma no encontrado']
    return JsonResponse(notFound, safe=False)












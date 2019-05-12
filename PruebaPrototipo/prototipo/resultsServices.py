from .models import *
import os
import csv
import json
from prototipo import spacyService as spacy
import prototipo.pictosServices as pictos
import django

django.setup()
from django.db import connection
import urllib
import base64
import pandas as pd


### SERVICIO QUE DADA UNA PALABRA Y UN NIVEL DEVUELVE SUS SINONIMOS FACILES  ###

def getEasySynonyms(word, level):
    dataJson = []
    ##  Devuelve todos los offsets de los synsets de dicha palabra
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')
    index = 1
    dataJson.insert(0, {'word': ""})
    dataJson[0]["word"] = word

    for offset in listOffsetToTheSynset:
        ##   Devuelve todos los sinónimos de esa palabra
        listaSynonyms = WeiSpa30Variant.objects.filter(offset=offset['offset']).values('word').distinct()
        #definition = WeiSpa30Synset.objects.filter(offset=offset).values('gloss')
        #example = WeiSpa30Examples.objects.filter(offset=offset).values('examples')

        ##   Por cada sinónimo, busca si se encuentra en la base de datos de las palabras fáciles
        listEasyWords = list()
        for synonym in listaSynonyms:
            if synonym['word'] != word:
                with connection.cursor() as cursor:
                    if level == "1":
                        cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s', [synonym['word']])
                    elif level == "2":
                        cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s', [synonym['word']])
                    else:
                        cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s', [synonym['word']])

                    result = cursor.fetchone()[0]
                    if result > 0:
                        listEasyWords.append(synonym['word'])

        if len(listEasyWords) > 0:
            dataJson.append({'offset': "", 'synonyms': []})  # , 'definition': "", 'example': "", 'picto': ""})
            dataJson[index]['offset'] = offset['offset']
            dataJson[index]['synonyms'] = listEasyWords

            index += 1
        '''    
        if definition[0]["gloss"] != "None":
            dataJson[0]["definition"] = definition[0]['gloss']
    
        if len(example) > 0:
            dataJson[0]["example"] = example[0]['examples']

        '''



    return dataJson


### SERVICIO QUEDADA UNA PALABRA Y UN NIVEL DEVUELVE SUS HIPONIMOS FACILES ###

def getEasyHyponyms(word, level):
    dataJson = []
    ##  Devuelve todos los offsets de los synsets de dicha palabra
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')
    index = 1
    dataJson.insert(0, {'word': ""})
    dataJson[0]["word"] = word

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
                                cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s',
                                               [hyponym['word']])
                            elif level == "2":
                                cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s',
                                               [hyponym['word']])
                            else:
                                cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s',
                                               [hyponym['word']])

                            result = cursor.fetchone()[0]
                            if result > 0:
                                listEasyWords.append(hyponym['word'])
            if len(listEasyWords) > 0:
                dataJson.append(
                    {'offsetFather': "", 'offset': "", 'hyponyms': []})  # , 'definition': "", 'example': "", 'picto': ""})
                dataJson[index]["offsetFather"] = offset['offset']
                dataJson[index]["offset"] = targetSynset["targetsynset"]
                dataJson[index]["hyponyms"] = listEasyWords

                index += 1
    return dataJson

### SERVICIO QUE DADA UNA PALABRA Y UN NIVEL DEVUELVE SUS HIPERONIMOS FACILES ###

def getEasyHyperonyms(word, level):
    dataJson = []
    ##  Devuelve todos los offsets de los synsets de dicha palabra
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')
    index = 1
    dataJson.insert(0, {'word': ""})
    dataJson[0]["word"] = word

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
                                cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s',
                                               [hyperonym['word']])
                            elif level == "2":
                                cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s',
                                               [hyperonym['word']])
                            else:
                                cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s',
                                               [hyperonym['word']])

                            result = cursor.fetchone()[0]
                            if result > 0:
                                listEasyWords.append(hyperonym['word'])
            if len(listEasyWords) > 0:
                dataJson.append(
                    {'offsetFather': "", 'offset': "", 'hyperonyms': []})  # , 'definition': "", 'example': "", 'picto': ""})
                dataJson[index]["offsetFather"] = offset['offset']
                dataJson[index]["offset"] = sourceSynset["sourcesynset"]
                dataJson[index]["hyperonyms"] = listEasyWords

                index += 1
    return dataJson


### SERVICIO QUE DADA UNA PALABRA Y UN NIVEL DEVUELVE UNA METÁFORA ###


def getMetaphor(word, level):

    dataJson = []
    repeatWords = set()
    ##  Devuelve todos los offsets de los synsets de dicha palabra
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')
    index = 1
    dataJson.insert(0, {'word': ""})
    dataJson[0]["word"] = word
    tipo, gender, number = spacy.genderAndNumberAPI(word)

    for offset in listOffsetToTheSynset:
        ##   Devuelve todos los sinónimos de esa palabra
        listaSynonyms = WeiSpa30Variant.objects.filter(offset=offset['offset']).values('word').distinct()
        #definition = WeiSpa30Synset.objects.filter(offset=offset).values('gloss')
        #example = WeiSpa30Examples.objects.filter(offset=offset).values('examples')

        ##   Por cada sinónimo, busca si se encuentra en la base de datos de las palabras fáciles
        listEasySynonymsWords = list()
        for synonym in listaSynonyms:

            if synonym['word'] != dataJson[0]['word']:

                with connection.cursor() as cursor:
                    if level == "1":

                        cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s', [synonym['word']])
                    elif level == "2":

                        cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s', [synonym['word']])
                    else:

                        cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s', [synonym['word']])

                    result = cursor.fetchone()[0]
                    if result > 0:
                        if synonym['word'] not in repeatWords:
                            repeatWords.add(synonym['word'])
                            tipoSinonimo, generoSinonimo, numeroSinonimo = spacy.genderAndNumberAPI(synonym['word'])
                            if tipoSinonimo == tipo:
                                listEasySynonymsWords.append(synonym['word'])


        phraseSynonym = list()
        if len(listEasySynonymsWords) > 0:
            dataJson.append({'type' : "SYNONYM", 'offset': "", 'metaphor': []})  # , 'definition': "", 'example': "", 'picto': ""})
            dataJson[index]['offset'] = offset['offset']
            for word in listEasySynonymsWords:
                phraseSynonym.append(spacy.phraseMaker(word))
                dataJson[index]['metaphor'] = phraseSynonym

            index += 1

        #print(dataJson)


    for offset in listOffsetToTheSynset:

        offsetMatchTargetSynset = (WeiSpa30Relation.objects.filter(targetsynset=offset['offset'], relation=12)).values(
            'sourcesynset').distinct()

        if len(offsetMatchTargetSynset) > 0:
            listEasyHyperonymsWords = list()
            for sourceSynset in offsetMatchTargetSynset:
                listaWordsHyperonyms = WeiSpa30Variant.objects.filter(offset=sourceSynset['sourcesynset']).values(
                    'word').distinct()
                for hyperonym in listaWordsHyperonyms:
                    if hyperonym['word'] != dataJson[0]['word']:

                        with connection.cursor() as cursor:
                            if level == "1":
                                cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s',
                                               [hyperonym['word']])
                            elif level == "2":
                                cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s',
                                               [hyperonym['word']])
                            else:
                                cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s',
                                               [hyperonym['word']])

                            result = cursor.fetchone()[0]
                            if result > 0:
                                if hyperonym['word'] not in repeatWords:
                                    tipoHiperonimo, generoHiperonimo, numeroHiperonimo = spacy.genderAndNumberAPI(
                                        hyperonym['word'])
                                    if tipoHiperonimo == tipo:
                                        repeatWords.add(hyperonym['word'])
                                        listEasyHyperonymsWords.append(hyperonym['word'])


        phraseHyperonym = list()
        if len(listEasyHyperonymsWords) > 0:
            #dataJson.append(
             #{"offsetHyperFather": "", 'offsetHyper': "", 'metaphorHyper': []})  # , 'definition': "", 'example': "", 'picto': ""})
            dataJson.append(
                {'type' : "HYPERONYM", 'offsetFather': "", 'offset': "", 'metaphor': []})  # , 'definition': "", 'example': "", 'picto': ""})
            dataJson[index]["offsetFather"] = offset['offset']
            dataJson[index]["offset"] = sourceSynset["sourcesynset"]
            for word in listEasyHyperonymsWords:
                phraseHyperonym.append(spacy.phraseMaker(word))
                dataJson[index]['metaphor'] = phraseHyperonym

            index += 1


    if len(dataJson) == 1:
        dataJson.pop()

    return dataJson


### SERVICIO QUE DADA UNA PALABRA Y UN NIVEL DEVUELVE UN SIMIL ###


def getSimil(word, level):
    dataJson = []
    repeatWords = set()
    ##  Devuelve todos los offsets de los synsets de dicha palabra
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')
    index = 1
    dataJson.insert(0, {'word': ""})
    dataJson[0]["word"] = word
    tipo, gender, number = spacy.genderAndNumberAPI(word)

    for offset in listOffsetToTheSynset:
        offsetMatchSourceSynset = (WeiSpa30Relation.objects.filter(sourcesynset=offset['offset'], relation=12)).values(
            'targetsynset').distinct()

        if len(offsetMatchSourceSynset) > 0:
            listEasyWords = list()
            for targetSynset in offsetMatchSourceSynset:
                listaWordsHyponyms = WeiSpa30Variant.objects.filter(offset=targetSynset['targetsynset']).values(
                    'word').distinct()

                for hyponym in listaWordsHyponyms:
                    if hyponym['word'] != dataJson[0]["word"]:


                        with connection.cursor() as cursor:
                            if level == "1":
                                print("ENTRO NIVEL 1")
                                cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s',
                                               [hyponym['word']])
                            elif level == "2":
                                print("ENTRO NIVEL 2")
                                cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s',
                                               [hyponym['word']])
                            else:
                                print("ENTRO NIVEL 3")
                                cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s',
                                               [hyponym['word']])

                            result = cursor.fetchone()[0]
                            if result > 0:
                                if hyponym['word'] not in repeatWords:
                                    tipoHiponimo, generoHiponimo, numeroHiponimo = spacy.genderAndNumberAPI(
                                        hyponym['word'])
                                    if tipo == tipoHiponimo:
                                        repeatWords.add(hyponym['word'])
                                        listEasyWords.append(hyponym['word'])

            phraseHyponym = list()
            if len(listEasyWords) > 0:
                dataJson.append(
                    {'offsetFather': "", 'offset': "",
                     'simil': []})  # , 'definition': "", 'example': "", 'picto': ""})
                dataJson[index]["offsetFather"] = offset['offset']
                dataJson[index]["offset"] = targetSynset["targetsynset"]
                for word in listEasyWords:
                    phraseHyponym.append(spacy.phraseMakerForHyponyms(word))
                    dataJson[index]['simil'] = phraseHyponym

                index += 1



    if len(dataJson) == 1:
        dataJson.pop()
    return dataJson



####    SERVICIO QUE DADA UNA PALABRA DEVUELVE TODOS SUS OFFSETS    ####


def getDefAndExample(word, level):
    dataJson = []

    repeatWords = set()
    ##  Devuelve todos los offsets de los synsets de dicha palabra
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')
    index = 1
    tipo, gender, number = spacy.genderAndNumberAPI(word)
    dataJson.insert(0, {'word' : ""})
    dataJson.insert(1, {"metaphor" : []})
    dataJson.insert(2, {"simil" : []})
    dataJson[0]["word"] = word
    i = 0
    i_simil = 0

    # SINONIMOS #
    for offset in listOffsetToTheSynset:
        ##   Devuelve todos los sinónimos de esa palabra
        listaSynonyms = WeiSpa30Variant.objects.filter(offset=offset['offset']).values('word').distinct()
        definition = WeiSpa30Synset.objects.filter(offset=offset['offset']).values('gloss')
        examples = WeiSpa30Examples.objects.filter(offset=offset['offset']).values('examples')

        ##   Por cada sinónimo, busca si se encuentra en la base de datos de las palabras fáciles
        listEasySynonymsWords = list()
        listExamples = list()
        for synonym in listaSynonyms:

            if synonym['word'] != dataJson[0]['word']:
                tipoSinonimo, generoSinonimo, numeroSinonimo = spacy.genderAndNumberAPI(synonym['word'])
                if tipoSinonimo == tipo:
                    with connection.cursor() as cursor:
                        if level == "1":

                            cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s', [synonym['word']])
                        elif level == "2":

                            cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s', [synonym['word']])
                        else:

                            cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s', [synonym['word']])

                        result = cursor.fetchone()[0]
                        if result > 0:
                            if synonym['word'] not in repeatWords:
                                repeatWords.add(synonym['word'])
                                listEasySynonymsWords.append(synonym['word'])


        if len(listEasySynonymsWords) > 0:
            print(examples)
            print(len(examples))

            if definition[0]["gloss"] != "None" or len(examples) > 0:
                dataJson[1]['metaphor'].append(({'type': "SYNONYM", 'offset': "", 'definition': "", 'example': []}))
                dataJson[1]['metaphor'][i]['offset'] = offset['offset']

                if definition[0]["gloss"] != "None":
                    dataJson[1]['metaphor'][i]["definition"] = definition[0]['gloss']
                    #print("DEF SINONIMOS")
                    #print(definition[0]["gloss"])
                    #print(definition)
                if len(examples) > 0:
                    for example in examples:
                        listExamples.append(example['examples'])
                    #print("EXAMPLE SINONIMOS")
                    #print(example)
                    dataJson[1]['metaphor'][i]["example"] = listExamples
                i += 1
                index += 1




    # HYPERONIMOS #
    for offset in listOffsetToTheSynset:

        offsetMatchTargetSynset = (WeiSpa30Relation.objects.filter(targetsynset=offset['offset'], relation=12)).values(
            'sourcesynset').distinct()

        if len(offsetMatchTargetSynset) > 0:
            listEasyHyperonymsWords = list()
            listExamplesHyper = list()
            for sourceSynset in offsetMatchTargetSynset:
                listaWordsHyperonyms = WeiSpa30Variant.objects.filter(offset=sourceSynset['sourcesynset']).values(
                    'word').distinct()
                definitionHyper = WeiSpa30Synset.objects.filter(offset=sourceSynset["sourcesynset"]).values('gloss')
                exampleHyper = WeiSpa30Examples.objects.filter(offset=sourceSynset["sourcesynset"]).values('examples')

                for hyperonym in listaWordsHyperonyms:
                    if hyperonym['word'] != dataJson[0]['word']:
                        tipoHiperonimo, generoHiperonimo, numeroHiperonimo = spacy.genderAndNumberAPI(hyperonym['word'])
                        if tipoHiperonimo == tipo:

                            with connection.cursor() as cursor:
                                if level == "1":
                                    cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s',
                                                   [hyperonym['word']])
                                elif level == "2":
                                    cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s',
                                                   [hyperonym['word']])
                                else:
                                    cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s',
                                                   [hyperonym['word']])

                                result = cursor.fetchone()[0]
                                if result > 0:
                                    if hyperonym['word'] not in repeatWords:
                                        repeatWords.add(hyperonym['word'])
                                        listEasyHyperonymsWords.append(hyperonym['word'])


            phraseHyperonym = list()
            if len(listEasyHyperonymsWords) > 0:
                #print(definitionHyper)
                #print(exampleHyper)
                if definitionHyper[0]["gloss"] != "None" or len(exampleHyper) > 0:

                    dataJson[1]['metaphor'].append(({'type': "HYPERONYM", 'offsetFather': "", 'offset': "", 'definition': "", 'example': []}))
                    dataJson[1]['metaphor'][i]['offsetFather'] = offset['offset']
                    dataJson[1]['metaphor'][i]['offset'] = sourceSynset["sourcesynset"]

                    if definitionHyper[0]['gloss'] != 'None':
                        #print("DEF HIPERONIMOS")
                        #print(definitionHyper)
                        dataJson[1]['metaphor'][i]["definition"] = definitionHyper[0]['gloss']

                    if len(exampleHyper) > 0:
                        for example in examples:
                            listExamplesHyper.append(example['examples'])
                        #print("EXAMPLE HIPERONIMOS")
                        #print(exampleHyper)
                        dataJson[1]['metaphor'][i]["example"] = listExamplesHyper
                    i += 1
                    index += 1


    # HIPONIMOS #
    for offset in listOffsetToTheSynset:

        offsetMatchSourceSynset = (WeiSpa30Relation.objects.filter(sourcesynset=offset['offset'], relation=12)).values(
            'targetsynset').distinct()

        if len(offsetMatchSourceSynset) > 0:
            listEasyWords = list()
            listExamplesHypo = list()
            for targetSynset in offsetMatchSourceSynset:

                listaWordsHyponyms = WeiSpa30Variant.objects.filter(offset=targetSynset['targetsynset']).values(
                    'word').distinct()
                definitionHypo = WeiSpa30Synset.objects.filter(offset=targetSynset["targetsynset"]).values('gloss')
                exampleHypo = WeiSpa30Examples.objects.filter(offset=targetSynset["targetsynset"]).values('examples')

                for hyponym in listaWordsHyponyms:
                    if hyponym['word'] != dataJson[0]["word"]:
                        tipoHiponimo, generoHiponimo, numeroHiponimo = spacy.genderAndNumberAPI(hyponym['word'])
                        if tipoHiponimo == tipo:
                            with connection.cursor() as cursor:
                                if level == "1":
                                    #print("ENTRO NIVEL 1")
                                    cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s',
                                                   [hyponym['word']])
                                elif level == "2":
                                    #print("ENTRO NIVEL 2")
                                    cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s',
                                                   [hyponym['word']])
                                else:
                                    #print("ENTRO NIVEL 3")
                                    cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s',
                                                   [hyponym['word']])

                                result = cursor.fetchone()[0]
                                if result > 0:
                                    if hyponym['word'] not in repeatWords:
                                        repeatWords.add(hyponym['word'])
                                        listEasyWords.append(hyponym['word'])



            if len(listEasyWords) > 0:

                if definitionHyper[0]["gloss"] != "None" or len(exampleHypo) > 0:
                    dataJson[2]['simil'].append(
                        ({'type': "HYPONYM", 'offsetFather': "", 'offset': "", 'definition': "", 'example': []}))

                    dataJson[2]['simil'][i_simil]['offsetFather'] = offset['offset']
                    dataJson[2]['simil'][i_simil]['offset'] = targetSynset["targetsynset"]


                    if definitionHypo[0]["gloss"] != "None":
                        if len(definitionHypo) > 0:
                            dataJson[2]['simil'][i_simil]["definition"] = definitionHypo[0]['gloss']

                    if len(exampleHypo) > 0:
                        for example in examples:
                            listExamplesHypo.append(example['examples'])
                        dataJson[2]['simil'][i_simil]["example"] = listExamplesHypo
                    i_simil += 1
                    index += 1



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
    # print("DATA ALL OFFSETS")
    # print(repr(dataJson))
    # print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson




















#    //-----------------------------------------------------------------------------------------------//    #

####    SERVICIO QUE DADA UNA PALABRA DEVUELVE TODOS SUS OFFSETS    ####

def allOffsets(word):
    dataJson = []
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')

    index = 0

    for offset in listOffsetToTheSynset:
        dataJson.insert(index, {'offset': ""})
        dataJson[index]["offset"] = offset['offset']
        index += 1
    # print("DATA ALL OFFSETS")
    # print(repr(dataJson))
    # print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson


#### SERVICIO QUE DADO UN OFFSET DEVUELVE TODOS LOS SINONIMOS   ####
def allSynonyms(offset):
    dataJson = []

    listaSynonyms = WeiSpa30Variant.objects.filter(offset=offset).values('word').distinct()
    definition = WeiSpa30Synset.objects.filter(offset=offset).values('gloss')
    example = WeiSpa30Examples.objects.filter(offset=offset).values('examples')

    dataJson.append({'offset': "", 'synonyms': [], 'definition': "", 'example': "", 'picto': ""})
    dataJson[0]['offset'] = offset

    for synonym in listaSynonyms:
        dataJson[0]['synonyms'].append(synonym['word'])

    if definition[0]["gloss"] != "None":
        dataJson[0]["definition"] = definition[0]['gloss']

    if len(example) > 0:
        dataJson[0]["example"] = example[0]['examples']

    # print("DATA ALL SYNONYMS")
    # print(json.dumps(dataJson ,ensure_ascii=False))
    # print(repr(dataJson))

    return dataJson


#### SERVICIO WEB QUE DADO UN OFFSET DEVUELVE SUS SINONIMOS FACILES     ####

def easySynonyms(word, offset):
    # print(offset)
    dataJson = []
    # archivo, csvarchivo = aperturaYlecturaCSV()
    listAllSynonyms = allSynonyms(offset)
    # jsonImage = pictos.getSynsetsAPI(word)

    for obj in listAllSynonyms:
        listEasyWords = list()
        for synonym in obj["synonyms"]:
            if synonym != word:
                with connection.cursor() as cursor:
                    # print(synonym)
                    cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s', [synonym])
                    result = cursor.fetchone()[0]
                    # print('RESULTADO')
                    # print(result)
                    # print(result)
                    if result > 0:
                        listEasyWords.append(synonym)

        '''

            csvarchivo.seek(0)
            for j in archivo:
                if synonym == j['PALABRA'] and synonym != word:
                    listEasyWords.append(j['PALABRA'])
        '''

        if len(listEasyWords) > 0:
            dataJson.insert(0, {'offset': "", 'easySynonyms': "", 'definition': "", 'example': "", 'picto': ""})
            dataJson[0]["easySynonyms"] = listEasyWords
            dataJson[0]["offset"] = obj["offset"]
            if dataJson[0]["definition"] != "None":
                dataJson[0]["definition"] = obj["definition"]
            dataJson[0]["example"] = obj["example"]
            img = urllib.request.urlopen('http://127.0.0.1:8000/imagenByPalabra/' + word)
            if img.info()['Content-Type'] != 'application/json':
                dataJson[0]["picto"] = 'http://127.0.0.1:8000/imagenByPalabra/' + word

            '''
            with connection.cursor() as cursor:
                cursor.execute('SELECT id_picto FROM pictos WHERE offset30 = %s',[offset])
                rows = cursor.fetchall()
                if len(rows) > 0:
                    dataJson[0]["picto"] = 'https://api.arasaac.org/api/pictograms/'+str(rows[0][0]) +'?download=false'
 
                if cursor.rowcount > 0:
                    image_64_decode = base64.decodebytes(cursor.fetchone()[0])
                    image_result = open('pictogramas/'+offset+'.png', 'wb')
                    image_result.write(image_64_decode)
                    image_result.close()
                    dataJson[0]["picto"] = 'pictogramas/'+offset+'.png'
                    '''

    # print("DATA EASY SYNONYMS")
    # print(json.dumps(dataJson, ensure_ascii=False))
    # print(dataJson)
    return dataJson


def makerSynonymsPhrase(word, offset):
    dataJson = []
    listEasySynonym = easySynonyms(word, offset)
    # print("LISTA")
    # print(listEasySynonym)
    index = 0
    for obj in listEasySynonym:
        listPhrase = list()
        for synonym in obj["easySynonyms"]:
            listPhrase.insert(index, spacy.phraseMaker(synonym))

        dataJson.insert(index, {'offset': "", 'phraseSynonyms': "", 'definition': "", 'example': "", 'picto': ""})
        dataJson[index]["phraseSynonyms"] = listPhrase
        dataJson[index]["offset"] = obj["offset"]
        dataJson[index]["definition"] = obj["definition"]
        dataJson[index]["example"] = obj["example"]
        dataJson[index]["picto"] = obj["picto"]
        index += 1
    # print(listPhrase)
    # print("DATA PHRASE SYNONYM")
    # print(repr(dataJson))
    # print(json.dumps(dataJson, ensure_ascii=False))
    # print('LLEGO')
    # print(dataJson)
    return dataJson


# ---------------------------------------------------------------------------------------------#

def allHyponyms(offset):
    dataJson = []

    offsetMatchSourceSynset = (WeiSpa30Relation.objects.filter(sourcesynset=offset, relation=12)).values(
        'targetsynset').distinct()
    # print(offsetMatchSourceSynset)
    if len(offsetMatchSourceSynset) > 0:
        index = 0
        for targetSynset in offsetMatchSourceSynset:

            dataJson.append(
                {'offsetFather': "", 'offset': "", 'hyponyms': [], 'definition': "", 'example': "", 'picto': ""})
            dataJson[index]["offsetFather"] = offset
            dataJson[index]["offset"] = targetSynset["targetsynset"]

            listaWordsHyponyms = WeiSpa30Variant.objects.filter(offset=targetSynset['targetsynset']).values(
                'word').distinct()

            listaAux = list()
            for hyponym in listaWordsHyponyms:
                listaAux.append(hyponym["word"])

            dataJson[index]["hyponyms"] = listaAux

            definition = WeiSpa30Synset.objects.filter(offset=targetSynset["targetsynset"]).values('gloss')
            example = WeiSpa30Examples.objects.filter(offset=targetSynset["targetsynset"]).values('examples')
            if definition[0]["gloss"] != "None":
                dataJson[index]["definition"] = definition[0]['gloss']

            if len(example) > 0:
                dataJson[index]["example"] = example[0]['examples']
            index += 1

    # print("DATA ALL SYNONYMS")
    # print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson


def easyHyponyms(word, offset):
    dataJson = []

    archivo, csvarchivo = aperturaYlecturaCSV()
    listAllHyponyms = allHyponyms(offset)
    jsonImage = pictos.getSynsetsAPI(word)

    for obj in listAllHyponyms:
        listEasyWords = list()
        for hyponym in obj["hyponyms"]:
            '''
            csvarchivo.seek(0)
            for j in archivo:
                if hyponym == j['PALABRA'] and hyponym != word:
                    listEasyWords.append(j['PALABRA'])
'''
            if hyponym != word:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s', [hyponym])
                    result = cursor.fetchone()[0]
                    if result > 0:
                        listEasyWords.append(hyponym)
        if len(listEasyWords) > 0:
            dataJson.insert(0, {'offsetFather': "", 'offset': "", 'easyHyponyms': "", 'definition': "", 'example': "",
                                'picto': ""})
            dataJson[0]["easyHyponyms"] = listEasyWords
            dataJson[0]["offsetFather"] = obj["offsetFather"]
            dataJson[0]["offset"] = obj["offset"]

            if dataJson[0]["definition"] != "None":
                dataJson[0]["definition"] = obj["definition"]
            dataJson[0]["example"] = obj["example"]
            img = urllib.request.urlopen('http://127.0.0.1:8000/imagenByPalabra/' + word)
            if img.info()['Content-Type'] != 'application/json':
                dataJson[0]["picto"] = 'http://127.0.0.1:8000/imagenByPalabra/' + word

            '''
                        with connection.cursor() as cursor:
                cursor.execute('SELECT id_picto FROM pictos WHERE offset30 = %s', [offset])
                rows = cursor.fetchall()
                if len(rows) > 0:
                    dataJson[0]["picto"] = 'https://api.arasaac.org/api/pictograms/' + str(rows[0][0]) + '?download=false'
            with connection.cursor() as cursor:
                cursor.execute('SELECT id_picto FROM pictos WHERE offset30 = %s', [offset])
                if cursor.rowcount > 0:
                    dataJson[0]["picto"] = 'https://api.arasaac.org/api/pictograms/' + str(cursor.fetchone()) + '?download=false'
'''

    # print("DATA EASY HYPONYMS")
    # print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson


def makerHyponymsPhrase(word, offset):
    dataJson = []
    listEasyHyponym = easyHyponyms(word, offset)
    # print("LISTA")
    # print(listEasySynonym)
    index = 0
    for obj in listEasyHyponym:
        listPhrase = list()
        for hyponym in obj["easyHyponyms"]:
            listPhrase.insert(index, spacy.phraseMakerForHyponyms(hyponym))

        dataJson.insert(index, {'offsetFather': "", 'offset': "", 'phraseHyponyms': "", 'definition': "", 'example': "",
                                'picto': ""})
        dataJson[index]["phraseHyponyms"] = listPhrase
        dataJson[index]["offset"] = obj["offset"]
        dataJson[index]["offsetFather"] = obj["offsetFather"]
        dataJson[index]["definition"] = obj["definition"]
        dataJson[index]["example"] = obj["example"]
        dataJson[index]["picto"] = obj["picto"]
        index += 1
    # print(listPhrase)
    # print("DATA PHRASE SYNONYM")
    # print(repr(dataJson))
    # print(json.dumps(dataJson, ensure_ascii=False))
    return dataJson


# ---------------------------------------------------------------------------------------------#

def allHyperonyms(offset):
    dataJson = []

    offsetMatchTargetSynset = (WeiSpa30Relation.objects.filter(targetsynset=offset, relation=12)).values(
        'sourcesynset').distinct()
    # print(offsetMatchSourceSynset)
    if len(offsetMatchTargetSynset) > 0:
        index = 0
        for sourceSynset in offsetMatchTargetSynset:

            dataJson.append(
                {'offsetFather': "", 'offset': "", 'hyperonyms': [], 'definition': "", 'example': "", 'picto': ""})
            dataJson[index]["offsetFather"] = offset
            dataJson[index]["offset"] = sourceSynset["sourcesynset"]

            listaWordsHyperonyms = WeiSpa30Variant.objects.filter(offset=sourceSynset['sourcesynset']).values(
                'word').distinct()

            listaAux = list()
            for hyperonym in listaWordsHyperonyms:
                listaAux.append(hyperonym["word"])

            dataJson[index]["hyperonyms"] = listaAux

            definition = WeiSpa30Synset.objects.filter(offset=sourceSynset["sourcesynset"]).values('gloss')
            example = WeiSpa30Examples.objects.filter(offset=sourceSynset["sourcesynset"]).values('examples')
            if definition[0]["gloss"] != "None":
                dataJson[index]["definition"] = definition[0]['gloss']

            if len(example) > 0:
                dataJson[index]["example"] = example[0]['examples']

            index += 1

    # print("DATA ALL HYPERONYMS")
    # print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson


def easyHyperonyms(word, offset):
    dataJson = []

    # archivo, csvarchivo = aperturaYlecturaCSV()
    listAllHyperonyms = allHyperonyms(offset)
    jsonImage = pictos.getSynsetsAPI(word)

    for obj in listAllHyperonyms:
        listEasyWords = list()
        for hyperonym in obj["hyperonyms"]:
            '''
            csvarchivo.seek(0)
            for j in archivo:
                if hyperonym == j['PALABRA'] and hyperonym != word:
                    listEasyWords.append(j['PALABRA'])
'''
            if hyperonym != word:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s', [hyperonym])
                    result = cursor.fetchone()[0]
                    if result > 0:
                        listEasyWords.append(hyperonym)
        if len(listEasyWords) > 0:
            dataJson.insert(0, {'offsetFather': "", 'offset': "", 'easyHyperonyms': "", 'definition': "", 'example': "",
                                'picto': ""})
            dataJson[0]["easyHyperonyms"] = listEasyWords
            dataJson[0]["offsetFather"] = obj["offsetFather"]
            dataJson[0]["offset"] = obj["offset"]

            if dataJson[0]["definition"] != "None":
                dataJson[0]["definition"] = obj["definition"]
            dataJson[0]["example"] = obj["example"]
            img = urllib.request.urlopen('http://127.0.0.1:8000/imagenByPalabra/' + word)
            if img.info()['Content-Type'] != 'application/json':
                dataJson[0]["picto"] = 'http://127.0.0.1:8000/imagenByPalabra/' + word

            # print(img.info()['Content-Type'])
            # dataJson[0]["picto"] =
            '''
            with connection.cursor() as cursor:
                cursor.execute('SELECT id_picto FROM pictos WHERE offset30 = %s', [offset])
                rows = cursor.fetchall()
                if len(rows) > 0:
                    dataJson[0]["picto"] = 'https://api.arasaac.org/api/pictograms/' + str(rows[0][0]) + '?download=false'
                    '''
        # if pictos.getImage(offset, jsonImage) != "None":
        # dataJson[0]["picto"] = pictos.getImage(offset, jsonImage)

    # print("DATA EASY HYPONYMS")
    # print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson


def makerHyperonymsPhrase(word, offset):
    dataJson = []
    listEasyHyperonym = easyHyperonyms(word, offset)
    # print("LISTA")
    # print(listEasySynonym)
    index = 0
    for obj in listEasyHyperonym:
        listPhrase = list()
        for hyperonym in obj["easyHyperonyms"]:
            listPhrase.insert(index, spacy.phraseMaker(hyperonym))

        dataJson.insert(index,
                        {'offsetFather': "", 'offset': "", 'phraseHyperonyms': "", 'definition': "", 'example': "",
                         'picto': ""})
        dataJson[index]["phraseHyperonyms"] = listPhrase
        dataJson[index]["offset"] = obj["offset"]
        dataJson[index]["offsetFather"] = obj["offsetFather"]
        dataJson[index]["definition"] = obj["definition"]
        dataJson[index]["example"] = obj["example"]
        dataJson[index]["picto"] = obj["picto"]
        index += 1
    # print(listPhrase)
    # print("DATA PHRASE SYNONYM")
    # print(repr(dataJson))
    # print(json.dumps(dataJson, ensure_ascii=False))
    return dataJson


def aperturaYlecturaCSV():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/5000PalabrasFiltradasYordenadas.csv', encoding="utf8", errors='ignore')

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    return archivo, csvarchivo





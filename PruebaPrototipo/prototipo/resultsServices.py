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
repeatWords = set()

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
        listEasySynonymsWords = list()
        for synonym in listaSynonyms:

            if synonym['word'] != dataJson[0]['word']:

                with connection.cursor() as cursor:
                    if level == "1":
                        cursor.execute('SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s AND tag = %s', [synonym['word'], tipo])
                    elif level == "2":

                        cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s AND tag = %s', [synonym['word'], tipo])
                    else:
                        cursor.execute('SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s AND tag = %s', [synonym['word'], tipo])

                    result = cursor.fetchone()[0]
                    if result > 0:
                        if synonym['word'] not in repeatWords:

                            repeatWords.add(synonym['word'])
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

                                cursor.execute(
                                    'SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyperonym['word'], tipo])
                            elif level == "2":

                                cursor.execute(
                                    'SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyperonym['word'], tipo])
                            else:
                                cursor.execute(
                                    'SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyperonym['word'], tipo])

                            result = cursor.fetchone()[0]
                            if result > 0:
                                if hyperonym['word'] not in repeatWords:

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
                                cursor.execute(
                                    'SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyponym['word'], tipo])
                            elif level == "2":
                                cursor.execute(
                                    'SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyponym['word'], tipo])
                            else:
                                cursor.execute(
                                    'SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyponym['word'], tipo])

                            result = cursor.fetchone()[0]
                            if result > 0:
                                if hyponym['word'] not in repeatWords:

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
                        with connection.cursor() as cursor:
                            if level == "1":

                                cursor.execute(
                                    'SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyponym['word'], tipo])
                            elif level == "2":

                                cursor.execute(
                                    'SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyponym['word'], tipo])
                            else:
                                cursor.execute(
                                    'SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyponym['word'], tipo])

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
                with connection.cursor() as cursor:
                    if level == "1":

                        cursor.execute(
                            'SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s AND tag = %s',
                            [synonym['word'], tipo])
                    elif level == "2":

                        cursor.execute(
                            'SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s AND tag = %s',
                            [synonym['word'], tipo])
                    else:
                        cursor.execute(
                            'SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s AND tag = %s',
                            [synonym['word'], tipo])

                    result = cursor.fetchone()[0]
                    if result > 0:
                        if synonym['word'] not in repeatWords:
                            repeatWords.add(synonym['word'])
                            listEasySynonymsWords.append(synonym['word'])


        if len(listEasySynonymsWords) > 0:
            #print(examples)
            #print(len(examples))

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


                        with connection.cursor() as cursor:
                            if level == "1":

                                cursor.execute(
                                    'SELECT COUNT(*) FROM 1000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyperonym['word'], tipo])
                            elif level == "2":

                                cursor.execute(
                                    'SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyperonym['word'], tipo])
                            else:
                                cursor.execute(
                                    'SELECT COUNT(*) FROM 10000_palabras_faciles WHERE word = %s AND tag = %s',
                                    [hyperonym['word'], tipo])

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


















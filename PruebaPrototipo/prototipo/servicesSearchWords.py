from .models import *
import os
import csv
import json
from prototipo import spacyService as spacy
import prototipo.pictosServices as pictos
import django
django.setup()
from django.db import connection
import base64
import pandas as pd



####    SERVICIO QUE DADA UNA PALABRA DEVUELVE TODOS SUS OFFSETS    ####

def allOffsets(word):

    dataJson = []
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')

    index = 0
    for offset in listOffsetToTheSynset:
        dataJson.insert(index, {'offset': ""})
        dataJson[index]["offset"] = offset['offset']
        index += 1
    #print("DATA ALL OFFSETS")
    #print(repr(dataJson))
    #print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson




#### SERVICIO QUE DADO UN OFFSET DEVUELVE TODOS LOS SINONIMOS   ####
def allSynonyms(offset):
    dataJson = []

    listaSynonyms = WeiSpa30Variant.objects.filter(offset=offset).values('word').distinct()
    definition = WeiSpa30Synset.objects.filter(offset=offset).values('gloss')
    example = WeiSpa30Examples.objects.filter(offset=offset).values('examples')


    dataJson.append({'offset': "", 'synonyms': [], 'definition' : "", 'example': "", 'picto': ""})
    dataJson[0]['offset'] = offset

    for synonym in listaSynonyms:
        dataJson[0]['synonyms'].append(synonym['word'])


    if definition[0]["gloss"] != "None":
        dataJson[0]["definition"] = definition[0]['gloss']


    if len(example) > 0:
        dataJson[0]["example"] = example[0]['examples']

    #print("DATA ALL SYNONYMS")
    #print(json.dumps(dataJson ,ensure_ascii=False))
    #print(repr(dataJson))

    return dataJson



#### SERVICIO WEB QUE DADO UN OFFSET DEVUELVE SUS SINONIMOS FACILES     ####

def easySynonyms(word, offset):
    #print(offset)
    dataJson = []
   # archivo, csvarchivo = aperturaYlecturaCSV()
    listAllSynonyms = allSynonyms(offset)
    #jsonImage = pictos.getSynsetsAPI(word)

    for obj in listAllSynonyms:
        listEasyWords = list()
        for synonym in obj["synonyms"]:
            if synonym != word:
                with connection.cursor() as cursor:
                    #print(synonym)
                    cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s',[synonym])
                    result = cursor.fetchone()[0]
                    #print('RESULTADO')
                    #print(result)
                    #print(result)
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
           #dataJson[0]["picto"] = pictos.getImage(offset, jsonImage)

           with connection.cursor() as cursor:
               cursor.execute('SELECT id_picto FROM pictos WHERE offset30 = %s',[offset])
               rows = cursor.fetchall()
               if len(rows) > 0:
                   dataJson[0]["picto"] = 'https://api.arasaac.org/api/pictograms/'+str(rows[0][0]) +'?download=false'
               '''
               if cursor.rowcount > 0:
                   image_64_decode = base64.decodebytes(cursor.fetchone()[0])
                   image_result = open('pictogramas/'+offset+'.png', 'wb')
                   image_result.write(image_64_decode)
                   image_result.close()
                   dataJson[0]["picto"] = 'pictogramas/'+offset+'.png'
                   '''

    #print("DATA EASY SYNONYMS")
    #print(json.dumps(dataJson, ensure_ascii=False))
    #print(dataJson)
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
    #print('LLEGO')
    #print(dataJson)
    return dataJson

#---------------------------------------------------------------------------------------------#

def allHyponyms(offset):
    dataJson = []

    offsetMatchSourceSynset = (WeiSpa30Relation.objects.filter(sourcesynset=offset, relation=12)).values(
        'targetsynset').distinct()
    #print(offsetMatchSourceSynset)
    if len(offsetMatchSourceSynset) > 0:
        index = 0
        for targetSynset in offsetMatchSourceSynset:

            dataJson.append({'offsetFather': "", 'offset': "", 'hyponyms': [], 'definition': "", 'example': "", 'picto': ""})
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

    #print("DATA ALL SYNONYMS")
    #print(json.dumps(dataJson ,ensure_ascii=False))
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
                    cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s',[hyponym])
                    result = cursor.fetchone()[0]
                    if result > 0:
                        listEasyWords.append(hyponym)
        if len(listEasyWords) > 0:
            dataJson.insert(0, {'offsetFather' : "",'offset': "", 'easyHyponyms': "", 'definition': "", 'example': "", 'picto': ""})
            dataJson[0]["easyHyponyms"] = listEasyWords
            dataJson[0]["offsetFather"] = obj["offsetFather"]
            dataJson[0]["offset"] = obj["offset"]

            if dataJson[0]["definition"] != "None":
                dataJson[0]["definition"] = obj["definition"]
            dataJson[0]["example"] = obj["example"]
            with connection.cursor() as cursor:
                cursor.execute('SELECT id_picto FROM pictos WHERE offset30 = %s', [offset])
                rows = cursor.fetchall()
                if len(rows) > 0:
                    dataJson[0]["picto"] = 'https://api.arasaac.org/api/pictograms/' + str(rows[0][0]) + '?download=false'
            '''
            with connection.cursor() as cursor:
                cursor.execute('SELECT id_picto FROM pictos WHERE offset30 = %s', [offset])
                if cursor.rowcount > 0:
                    dataJson[0]["picto"] = 'https://api.arasaac.org/api/pictograms/' + str(cursor.fetchone()) + '?download=false'
'''

    #print("DATA EASY HYPONYMS")
    #print(json.dumps(dataJson ,ensure_ascii=False))
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

        dataJson.insert(index, {'offsetFather' : "", 'offset': "", 'phraseHyponyms': "", 'definition': "", 'example': "", 'picto': ""})
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




#---------------------------------------------------------------------------------------------#

def allHyperonyms(offset):
    dataJson = []

    offsetMatchTargetSynset = (WeiSpa30Relation.objects.filter(targetsynset=offset, relation=12)).values(
        'sourcesynset').distinct()
    # print(offsetMatchSourceSynset)
    if len(offsetMatchTargetSynset) > 0:
        index = 0
        for sourceSynset in offsetMatchTargetSynset:

            dataJson.append({'offsetFather': "", 'offset': "", 'hyperonyms': [], 'definition': "", 'example': "", 'picto': ""})
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

    #print("DATA ALL HYPERONYMS")
    #print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson


def easyHyperonyms(word, offset):
    dataJson = []

    #archivo, csvarchivo = aperturaYlecturaCSV()
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
                    cursor.execute('SELECT COUNT(*) FROM 5000_palabras_faciles WHERE word = %s',[hyperonym])
                    result = cursor.fetchone()[0]
                    if result > 0:
                        listEasyWords.append(hyperonym)
        if len(listEasyWords) > 0:
            dataJson.insert(0, {'offsetFather' : "",'offset': "", 'easyHyperonyms': "", 'definition': "", 'example': "", 'picto': ""})
            dataJson[0]["easyHyperonyms"] = listEasyWords
            dataJson[0]["offsetFather"] = obj["offsetFather"]
            dataJson[0]["offset"] = obj["offset"]

            if dataJson[0]["definition"] != "None":
                dataJson[0]["definition"] = obj["definition"]
            dataJson[0]["example"] = obj["example"]
            with connection.cursor() as cursor:
                cursor.execute('SELECT id_picto FROM pictos WHERE offset30 = %s', [offset])
                rows = cursor.fetchall()
                if len(rows) > 0:
                    dataJson[0]["picto"] = 'https://api.arasaac.org/api/pictograms/' + str(rows[0][0]) + '?download=false'
           # if pictos.getImage(offset, jsonImage) != "None":
               # dataJson[0]["picto"] = pictos.getImage(offset, jsonImage)

    #print("DATA EASY HYPONYMS")
    #print(json.dumps(dataJson ,ensure_ascii=False))
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

        dataJson.insert(index, {'offsetFather' : "", 'offset': "", 'phraseHyperonyms': "", 'definition': "", 'example': "", 'picto': ""})
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





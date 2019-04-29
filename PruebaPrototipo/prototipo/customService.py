from .models import *
import os
import csv
import json
from prototipo import spacyService as spacy
import prototipo.pictosServices as pictos
import pandas as pd
import time

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


def customSynonyms(word, offset, jsonImage):
    dataJson = []
    #archivo, csvarchivo = aperturaYlecturaCSV()
    listAllSynonyms = allSynonyms(offset)
    #jsonImage = pictos.getSynsetsAPI(word)
    #print(listAllSynonyms)
    #listaSynonyms = WeiSpa30Variant.objects.filter(offset=offset).values('word').distinct()
    #definition = WeiSpa30Synset.objects.filter(offset=offset).values('gloss')
    #example = WeiSpa30Examples.objects.filter(offset=offset).values('examples')

    df = pd.DataFrame(listAllSynonyms)


    for obj in listAllSynonyms:

        listEasyWords = list()
        listPhrase = list()
        for synonym in obj["synonyms"]:
            #csvarchivo.seek(0)
            archivo, csvarchivo = aperturaYlecturaCSV()
            start_time = time.time()
            for j in archivo:
                if synonym == j['PALABRA'] and synonym != word:
                    listEasyWords.append(j['PALABRA'])
                    listPhrase.append(spacy.phraseMaker(synonym))
            csvarchivo.close()
            print('T VUELTA')
            print(time.time() - start_time)
        #print(listPhrase)
        if len(listEasyWords) > 0:
            start2 = time.time()
            dataJson.insert(0, {'offset': "", 'easySynonyms': "", 'definition': "", 'example': "", 'picto': "", 'phraseSynonyms': ""})
            dataJson[0]["easySynonyms"] = listEasyWords
            dataJson[0]["offset"] = obj["offset"]
            if dataJson[0]["definition"] != "None":
                dataJson[0]["definition"] = obj["definition"]
            dataJson[0]["example"] = obj["example"]
            #url = pictos.getImage(offset, jsonImage)
            url = "None"
            if url != "None":
                dataJson[0]["picto"] = url
            dataJson[0]["phraseSynonyms"] = listPhrase
            print('T JSON')
            print(time.time() - start2)
    return dataJson

def customHyponyms(word, offset, jsonImage):
    dataJson = []

    #archivo, csvarchivo = aperturaYlecturaCSV()
    listAllHyponyms = allHyponyms(offset)
    #jsonImage = pictos.getSynsetsAPI(word)

    for obj in listAllHyponyms:
        listEasyWords = list()
        listPhrase = list()
        for hyponym in obj["hyponyms"]:
            #csvarchivo.seek(0)
            archivo, csvarchivo = aperturaYlecturaCSVIndice(hyponym[0])
            for j in archivo:
                if hyponym == j['PALABRA'] and hyponym != word:
                    listEasyWords.append(j['PALABRA'])
                    listPhrase.append(spacy.phraseMakerForHyponyms(hyponym))
            csvarchivo.close()

        if len(listEasyWords) > 0:
            dataJson.insert(0, {'offsetFather' : "",'offset': "", 'easyHyponyms': "", 'definition': "", 'example': "", 'picto': "", 'phraseHyponyms': ""})
            dataJson[0]["easyHyponyms"] = listEasyWords
            dataJson[0]["offsetFather"] = obj["offsetFather"]
            dataJson[0]["offset"] = obj["offset"]

            if dataJson[0]["definition"] != "None":
                dataJson[0]["definition"] = obj["definition"]
            dataJson[0]["example"] = obj["example"]
            #url = pictos.getImage(offset, jsonImage)
            url = "None"
            if url != "None":
                dataJson[0]["picto"] = url
            dataJson[0]["phraseHyponyms"] = listPhrase

    #print("DATA EASY HYPONYMS")
    #print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson

def customHyperonyms(word, offset, jsonImage):
    dataJson = []

    #archivo, csvarchivo = aperturaYlecturaCSV()
    listAllHyperonyms = allHyperonyms(offset)
    #jsonImage = pictos.getSynsetsAPI(word)

    for obj in listAllHyperonyms:
        listEasyWords = list()
        listPhrase = list()
        for hyperonym in obj["hyperonyms"]:
            #csvarchivo.seek(0)
            archivo, csvarchivo = aperturaYlecturaCSVIndice(hyperonym[0])
            for j in archivo:
                if hyperonym == j['PALABRA'] and hyperonym != word:
                    listEasyWords.append(j['PALABRA'])
                    listPhrase.append(spacy.phraseMaker(hyperonym))
            csvarchivo.close()

        if len(listEasyWords) > 0:
            dataJson.insert(0, {'offsetFather' : "",'offset': "", 'easyHyperonyms': "", 'definition': "", 'example': "", 'picto': "", 'phraseHyperonyms': ""})
            dataJson[0]["easyHyperonyms"] = listEasyWords
            dataJson[0]["offsetFather"] = obj["offsetFather"]
            dataJson[0]["offset"] = obj["offset"]

            if dataJson[0]["definition"] != "None":
                dataJson[0]["definition"] = obj["definition"]
            dataJson[0]["example"] = obj["example"]
            #url = pictos.getImage(offset, jsonImage)
            url = "None"
            if url != "None":
                dataJson[0]["picto"] = url
            dataJson[0]["phraseHyperonyms"] = listPhrase

    #print("DATA EASY HYPONYMS")
    #print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson



def aperturaYlecturaCSV():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/5000PALABRASFILTRADAS.csv', encoding="utf8", errors='ignore')

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    return archivo, csvarchivo

def aperturaYlecturaCSVIndice(letra):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/indices/5000PalabrasFiltradasYordenadas_'+letra+'.csv', encoding="utf8", errors='ignore')

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    return archivo, csvarchivo

def loadIndex():
    index = dict()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/index.csv', encoding="utf8", errors='ignore')
    archivo = csv.DictReader(csvarchivo, delimiter=";")

    for i in archivo:
        #print(i)
        index.update({i['LETRA']:i['INICIO']})

    #print(csvarchivo.seek())


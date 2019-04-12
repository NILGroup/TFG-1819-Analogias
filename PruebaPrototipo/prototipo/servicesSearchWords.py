from .models import *
import os
import csv
import json
from prototipo import spacyService as spacy

def findOffsetsToTheSynsets(word):
    listEasyWords = list()
    '''
    # Primero busca que palabras son iguales a la palabra de entrada y nos quedamos con la columna offset
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).only('offset')
    listDictSynset = list()
    listEasyWords = list()
    #print(listOffsetToTheSynset)

    for offset in listOffsetToTheSynset.values():
        #print(offset['offset'])
        results= dict(sinonimos="", hiponimos="", hiperonimos="")

        listSynonyms = searchWord(offset['offset'])
        #listHyponyms = searchHyponyms(offset['offset'])
        #listHyperonyms = searchHyperonyms(offset['offset'])

        results["sinonimos"] = listSynonyms
        #results["hiponimos"] = listHyponyms
        #results["hiperonimos"] = listHyperonyms

        listDictSynset.append(results)

    #print(listDictSynset)




    for index in listDictSynset:
        resultsAux = dict(synonyms="", hyponyms="", hyperonyms="")
        resultSynonymsInMatch = findMatchInPalabrasRAE(index["sinonimos"])
        resultHyperonymsInMatch = findMatchInPalabrasRAE(index["hiperonimos"])
        resultHyponymsInMatch = findMatchInPalabrasRAE(index["hiponimos"])

        resultsAux["synonyms"] = resultSynonymsInMatch
        resultsAux["hyperonyms"] = resultHyperonymsInMatch
        resultsAux["hyponyms"] = resultHyponymsInMatch

        listEasyWords.append(resultsAux)

    #print(listEasyWords)
    '''
    return listEasyWords





### SERVICIO QUE DADA UNA PALABRA DEVUELVE TODOS SUS SINONIMOS  ###
def searchAllSynonyms(word):
    #LISTA DE OFFSETS DE CADA UNA DE LAS ACEPCIONES DE LA PALABRA BUSCADA
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).values('offset')

    dataJson = []
    for offset in listOffsetToTheSynset.values():
        #LISTA PALABRAS QUE CONTIENE EL OFFSET
        listaWords = WeiSpa30Variant.objects.filter(offset=offset['offset']).values('word').distinct()

        #LISTA DE OFFSET PERTENECIENTES A CADA UNA DE LAS PALABRAS QUE CONTIENE EL OFFSET
        listaOffset = WeiSpa30Variant.objects.filter(offset=offset['offset']).values('offset').distinct()

        definition = WeiSpa30Synset.objects.filter(offset=offset['offset']).values('gloss')
        example = WeiSpa30Examples.objects.filter(offset=offset['offset']).values('examples')
        #print(definition[0]['gloss'])
        #if len(example) > 0:
            #print(example[0]['examples'])

        index = 0
        for i in listaOffset:
           dataJson.insert(index, {'offset': "", 'synonyms': [], 'definition' : "", 'example' : ""})
           dataJson[index]["offset"] = i["offset"]

           #METE LA DEFINICION, SI NO HAY DEF NO METE NADA
           if dataJson[index]["definition"] != 'None':
            dataJson[index]["definition"] = definition[0]['gloss']

           #EN ESTE CASO, SI NO HAY EJEMPLO, ESA ENTRADA DE LA TABLA ESTA VACIA POR ESO HAY QUE COMPROBAR SI HAY EJEMPLO O NO
           #CON EL LEN > 0 PORQUE SI NO HAY Y LO INTENTAS METER CASCA
           if len(example) > 0:
               dataJson[index]["example"] = example[0]['examples']

           for value in listaWords:
               dataJson[index]["synonyms"].append(value["word"])
               #wordsReturned.append(value)
           index += 1

    #print("DATA")
    #print(repr(dataJson))
    #print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson



###   SERVICIO WEB QUE DADA UNA PALABRA DEVUELVE LOS SINONIMOS FACILES  ###
def findEasySynonyms(word):
    archivo, csvarchivo = aperturaYlecturaCSV()
    dataJson = []
    listSynonyms = searchAllSynonyms(word)
    #print(listSynonyms)

    index = 0

    for i in listSynonyms:
        listEasyWords = list()
        for x in i["synonyms"]:
            csvarchivo.seek(0)
            for j in archivo:
                if x == j['PALABRA'] and x != word:
                    listEasyWords.append(j['PALABRA'])

        if len(listEasyWords) > 0:
            dataJson.insert(index, {'offset': "", 'easySynonyms': "", 'definition' : "", 'example' : ""})
            dataJson[index]["easySynonyms"] = listEasyWords
            dataJson[index]["offset"] = i["offset"]
            if dataJson[index]["definition"] != None:
                dataJson[index]["definition"] = i["definition"]
            dataJson[index]["example"] = i["example"]
            index += 1

    #print("DATA")
    #print(repr(dataJson))
    #print(json.dumps(dataJson, ensure_ascii=False))

    return dataJson



###   SERVICIO WEB QUE DADA UNA PALABRA DEVUELVE LA FRASE FORMADA CON EL SINONIMO  ###
def phraseSynonym(word):
    dataJson = []
    listEasySynonym = findEasySynonyms(word)
    #print("LISTA")
    #print(listEasySynonym)
    index = 0
    for obj in listEasySynonym:
        listPhrase = list()
        for synonym in obj["easySynonyms"]:
            listPhrase.insert(index, spacy.phraseMakerSynonym(synonym))

        dataJson.insert(index, {'offset': "", 'phraseSynonyms': "", 'definition' : "", 'example' : ""})
        dataJson[index]["phraseSynonyms"] = listPhrase
        dataJson[index]["offset"] = obj["offset"]
        dataJson[index]["definition"] = obj["definition"]
        dataJson[index]["example"] = obj["example"]
        index += 1
    #print(listPhrase)
    print("DATA")
    #print(repr(dataJson))
    print(json.dumps(dataJson, ensure_ascii=False))
    return dataJson




def searchAllHyponyms(word):
    listOffsetToTheSynset = searchAllSynonyms(word)
    dataJson = []
    index = 0
    for offset in listOffsetToTheSynset:
        offsetMatchSourceSynset = (WeiSpa30Relation.objects.filter(sourcesynset=offset["offset"], relation=12)).values('targetsynset').distinct()


        if len(offsetMatchSourceSynset) > 0:

            listFinal = list()
            for targetSynset in offsetMatchSourceSynset:
                dataJson.insert(index, {'offsetPather': "", 'offset': "", 'hyponyms': [], 'definition' : "", 'example' : ""})
                dataJson[index]["offsetPather"] = offset["offset"]
                listFinal.insert(index, targetSynset["targetsynset"])
                dataJson[index]["offset"] = targetSynset["targetsynset"]

                listaWordsHyponyms = WeiSpa30Variant.objects.filter(offset=targetSynset['targetsynset']).values('word').distinct()

                listaAux = list()
                for hyponym in listaWordsHyponyms:
                    listaAux.append(hyponym["word"])

                dataJson[index]["hyponyms"] = listaAux


            index += 1

    #print("DATA")
    #print(repr(dataJson))
    #print(json.dumps(dataJson ,ensure_ascii=False))
    return dataJson



def searchHyponyms(offset):

    offsetMatchSourceSynset = (WeiSpa30Relation.objects.filter(sourcesynset=offset) & (
        WeiSpa30Relation.objects.filter(relation=12)))

    words = list()
    for value in offsetMatchSourceSynset:
        words_aux = searchAllSynonyms(value.targetsynset)
        for word in words_aux:
            words.append(word)
    return words


def aperturaYlecturaCSV():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/5000PalabrasFiltradas.csv', encoding="utf8", errors='ignore')

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    return archivo, csvarchivo





def searchHyperonyms(offset):

    offsetMatchTargetSynset = (WeiSpa30Relation.objects.filter(targetsynset=offset) & (
        WeiSpa30Relation.objects.filter(relation=12)))
    words = list()
    for value in offsetMatchTargetSynset:
        words_aux = searchAllSynonyms(value.sourcesynset)
        for word in words_aux:
            words.append(word)
    return words



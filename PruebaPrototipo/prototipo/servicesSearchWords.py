from .models import WeiSpa30Variant, WeiSpa30Relation
import os
import csv
import json

def findOffsetsToTheSynsets(word):

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
    return listEasyWords





#SERVICIO QUE DADO UN OFFSET DEVUELVE TODOS SUS SINONIMOS
def searchWord(offset):

   listaWords = WeiSpa30Variant.objects.filter(offset=offset).values('word').distinct()
   listaOffset = WeiSpa30Variant.objects.filter(offset=offset).values('offset').distinct()
   #print("LISTA OFFSET")
   #print(listaOffset)
   #print("LISTA WORDS")
   #print(listaOffset)
   wordsReturned = list()
   json = []
   index = 0
   for i in listaOffset:
       json.insert(index, {'offset': "", 'synonyms': []})
       json[index]["offset"] = i
       for value in listaWords:

           json[index]["synonyms"] = value
           wordsReturned.append(value)
       index += 1

   print("DATA")
   print(repr(json))
   return wordsReturned



def searchHyponyms(offset):

    offsetMatchSourceSynset = (WeiSpa30Relation.objects.filter(sourcesynset=offset) & (
        WeiSpa30Relation.objects.filter(relation=12)))

    words = list()
    for value in offsetMatchSourceSynset:
        words_aux = searchWord(value.targetsynset)
        for word in words_aux:
            words.append(word)
    return words



def searchHyperonyms(offset):

    offsetMatchTargetSynset = (WeiSpa30Relation.objects.filter(targetsynset=offset) & (
        WeiSpa30Relation.objects.filter(relation=12)))
    words = list()
    for value in offsetMatchTargetSynset:
        words_aux = searchWord(value.sourcesynset)
        for word in words_aux:
            words.append(word)
    return words



def findMatchInPalabrasRAE(listSynonyms):
    #print("SINONIMOS QUE ENTRAN EN FINDMATCH " + str(listSynonyms))
    archivo, csvarchivo = aperturaYlecturaCSV()
    listEasyWords = list()
    for i in listSynonyms:
        csvarchivo.seek(0)
        for j in archivo:
            #print("PALABRA A BUSCAR FINDMATCH " + str(i))
            if i == j['PALABRA']:
                listEasyWords.append(j['PALABRA'])

    #print("SINONIMOS QUE DEVUELVE FINDMATCH " + str(listEasyWords))
    return listEasyWords



def aperturaYlecturaCSV():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/5000PalabrasFiltradas.csv', encoding="utf8", errors='ignore')

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    return archivo, csvarchivo
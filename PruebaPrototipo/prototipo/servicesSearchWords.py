from .models import WeiSpa30Variant, WeiSpa30Relation
import os
import csv

def findOffsetsToTheSynsets(word):

    # Primero busca que palabras son iguales a la palabra de entrada y nos quedamos con la columna offset
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).only('offset')
    listDictSynset = list()
    listEasyWords = set()


    for offset in listOffsetToTheSynset.values():
        results= dict(sinonimos="", hiponimos="", hiperonimos="")

        listSynonyms = searchWord(offset['offset'])
        listHyponyms = searchHyponyms(offset['offset'])
        listHyperonyms = searchHyperonyms(offset['offset'])

        results["sinonimos"] = listSynonyms
        results["hiponimos"] = listHyponyms
        results["hiperonimos"] = listHyperonyms

        listDictSynset.append(results)



    #print(listDictSynset)
    resultsAux = dict(synonyms="", hyponyms="", hyperonyms="")
    for index in listDictSynset:
        resultsAux["synonyms"] = list(findMatchInPalabrasRAE(index["sinonimos"]))
        resultsAux["hyponyms"] = findMatchInPalabrasRAE(index["hiponimos"])
        resultsAux["hyperonyms"] = findMatchInPalabrasRAE(index["hiperonimos"])


    #print("HOLIIII " + str(resultsAux))

    #print(listDictSynset)
    return resultsAux






def searchWord(offset):

   listaWords = WeiSpa30Variant.objects.filter(offset=offset)
   wordsReturned = list()
   for value in listaWords:
       wordsReturned.append(value.word)

   return wordsReturned



def searchHyponyms(offset):

    offsetMatchSourceSynset = (WeiSpa30Relation.objects.filter(sourcesynset=offset) & (
        WeiSpa30Relation.objects.filter(relation=12)))
    listaTargetSynset = list()

    words = list()
    for value in offsetMatchSourceSynset:

        #listaTargetSynset.append(value.targetsynset)
        words.append(searchWord(value.targetsynset))
        #print(words)

   # for i in words:
    #    for a in i:
     #       print("PRUEBA RESULTADO" + str(a))
    return words


def searchHyperonyms(offset):

    offsetMatchTargetSynset = (WeiSpa30Relation.objects.filter(targetsynset=offset) & (
        WeiSpa30Relation.objects.filter(relation=12)))
    listaSourceSynset = list()
    words = list()
    for value in offsetMatchTargetSynset:
        #listaSourceSynset.append(value.sourcesynset)
        words.append(searchWord(value.sourcesynset))
    return words



def findMatchInPalabrasRAE(listSynonyms):
    #print("SINONIMOSSSSSSSSSS " + str(listSynonyms))
    archivo, csvarchivo = aperturaYlecturaCSV()
    listEasyWords = set()
    for i in listSynonyms:
        csvarchivo.seek(0)
        for j in archivo:
            if i == j['PALABRA']:
                listEasyWords.add(j['PALABRA'])


    return listEasyWords



def aperturaYlecturaCSV():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csvarchivo = open(BASE_DIR + '/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')

    archivo = csv.DictReader(csvarchivo, delimiter=";")

    return archivo, csvarchivo
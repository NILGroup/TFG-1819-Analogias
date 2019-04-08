from .models import WeiSpa30Variant, WeiSpa30Relation
import os
import csv

def findOffsetsToTheSynsets(word):

    # Primero busca que palabras son iguales a la palabra de entrada y nos quedamos con la columna offset
    listOffsetToTheSynset = WeiSpa30Variant.objects.filter(word=word).only('offset')
    listDictSynset = list()

    for offset in listOffsetToTheSynset.values():
        results = dict(sinonimos="", hiponimos="", hiperonimos="")
        listSynonyms = searchSynonyms(offset['offset'])
        listHyponyms = searchHyponyms(offset['offset'])
        results["sinonimos"] = listSynonyms
        results["hiponimos"] = listHyponyms
        listDictSynset.append(results)

    print(listDictSynset)
    return listDictSynset






def searchSynonyms(offset):

    synonymsInSynset = (WeiSpa30Variant.objects.filter(offset=offset))
    listSynonymsSynset = list()
    for value in synonymsInSynset:
        listSynonymsSynset.append(value.word)
    return listSynonymsSynset



def searchHyponyms(offset):

    offsetMatchSourceSynset = (WeiSpa30Relation.objects.filter(sourcesynset=offset) & (
        WeiSpa30Relation.objects.filter(relation=12)))
    listaTargetSynset = list()
    words = list()
    for value in offsetMatchSourceSynset:
        listaTargetSynset.append(value.targetsynset)
        words = searchWord(value.targetsynset)
    return words




def searchWord(offset):

   listaWords = WeiSpa30Variant.objects.filter(offset=offset)
   wordsReturned = list()

   for value in listaWords:
       wordsReturned.append(value.word)

   return wordsReturned
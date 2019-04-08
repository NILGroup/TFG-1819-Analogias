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
        #listHyponims = searchHyponym()
        results["sinonimos"] = listSynonyms
        listDictSynset.append(results)

    print(listDictSynset)
    return listDictSynset






def searchSynonyms(offset):

    synonymsInSynset = (WeiSpa30Variant.objects.filter(offset=offset))
    listSynonymsSynset = list()
    for value in synonymsInSynset:
        listSynonymsSynset.append(value.word)
    return listSynonymsSynset


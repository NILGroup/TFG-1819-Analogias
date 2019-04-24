import requests
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
import django
django.setup()
from prototipo.models import *
import csv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import prototipo.servicesSearchWords as services

def main():
    csvsalida = open('pictos.csv', 'w', encoding="utf8", newline='')
    salida = csv.writer(csvsalida, delimiter=";")
    salida.writerow(("PALABRA", "OFFSET3.1", "OFFSET3.0","IDPICTO"))
    f = open('lista.txt','r' ,encoding="utf8", newline="")
    data = f.readlines()
    for line in data:
        #print(line.rstrip('\n'))
        execute(str(line.rstrip('\n')), salida)


    csvsalida.close()



'''
def allOffsets(word):
    #print(word)
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
'''
def getSynsetsAPI(word):

    jsonAPI = requests.get('https://api.arasaac.org/api/pictograms/es/search/' + word,  verify=False).json()



        #Ahoraa hay que coger cada synset y hacer otra peticion a http://wordnet-rdf.princeton.edu/json/id/synset y con los resultados
        #del json mirar el campo pwn30, si este coincide
    return jsonAPI


def getImage(offset, json, word):
    for synsets in json:
        #print("HOLA")
        #print(synsets["synsets"])
        #print(synsets["idPictogram"])
        for synset in synsets["synsets"]:
            jsonWrdnet = requests.get('https://wordnet-rdf.princeton.edu/json/id/' + synset, verify=False).json()
            #print('UNA COSA')
            #print('spa-30-'+jsonWrdnet[0]['old_keys']['pwn30'][0])
            #print('LA OTRA')
            #print(offset)
            if (offset == 'spa-30-'+jsonWrdnet[0]['old_keys']['pwn30'][0]):
               # print('ENTRO')
                #print(offset)
                #return requests.get('https://api.arasaac.org/api/pictograms/'+str(synsets["idPictogram"]) +'?download=false' , verify=False)
                return word, synset, offset, synsets["idPictogram"]
                #print(image)

    return "None","None","None","None"




def execute(word, salida):
    print(word)
    offsets = services.allOffsets(word)
    print(offsets)
    jsonImage = getSynsetsAPI(word)
    for offset in offsets:
        word, synset, offset, id = getImage(offset['offset'], jsonImage, word)
        #print(word, synset, offset, id)
        if word != "None":

            salida.writerow((word, synset, offset, id))

main()
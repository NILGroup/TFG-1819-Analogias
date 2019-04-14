import requests

def getSynsetsAPI(word, offset):
    dataJson = []

    jsonAPI = requests.get('https://api.arasaac.org/api/pictograms/es/search/' + word,  verify=False).json()

    for synset in jsonAPI:
        print(synset["synsets"])
        #Ahoraa hay que coger cada synset y hacer otra peticion a http://wordnet-rdf.princeton.edu/json/id/synset y con los resultados
        #del json mirar el campo pwn30, si este coincide
    return dataJson
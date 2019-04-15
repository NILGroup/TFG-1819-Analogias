import requests


#DADA UNA PALABRA OBTIENE EL JSON CON TODOS LOS DATOS DE ARASAAC
def getSynsetsAPI(word):

    jsonAPI = requests.get('https://api.arasaac.org/api/pictograms/es/search/' + word,  verify=False).json()



        #Ahoraa hay que coger cada synset y hacer otra peticion a http://wordnet-rdf.princeton.edu/json/id/synset y con los resultados
        #del json mirar el campo pwn30, si este coincide
    return jsonAPI


def getImage(offset, json):
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
                return 'https://api.arasaac.org/api/pictograms/'+str(synsets["idPictogram"]) +'?download=false'
                #print(image)

    return "None"


def getOneImage(offset, synsets):
    for synset in synsets:
        jsonWrdnet = requests.get('https://wordnet-rdf.princeton.edu/json/id/' + synset, verify=False).json()
        # print('UNA COSA')
        # print('spa-30-'+jsonWrdnet[0]['old_keys']['pwn30'][0])
        # print('LA OTRA')
        # print(offset)
        if (offset == 'spa-30-' + jsonWrdnet[0]['old_keys']['pwn30'][0]):
            #print('ENTRO')
            #print(offset)
            # return requests.get('https://api.arasaac.org/api/pictograms/'+str(synsets["idPictogram"]) +'?download=false' , verify=False)
            return 'https://api.arasaac.org/api/pictograms/' + str(synsets["idPictogram"]) + '?download=false'
    return "None"
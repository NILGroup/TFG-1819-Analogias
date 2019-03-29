import spacy
import csv
import requests







nlp = spacy.load('es_core_news_sm')

data = list()
cont = 1

csvarchivo = open('10000PALABRAS.csv', encoding="utf8", errors='ignore')
entrada = csv.reader(csvarchivo, delimiter=";")
csvsalida = open('10000PalabrasFiltradas.csv', 'w', encoding="utf8", newline="")
salida = csv.writer(csvsalida, delimiter=";")

salida.writerow(("NUMERO", "PALABRA", "TAG"))

for i in entrada:
    #print(i)
    data.append(i[1])

cont = 1
for i in data:
    doc = nlp(i)

    for token in doc:
        if token.pos_ == "ADV" or token.pos_ == "NOUN" or token.pos_ == "AUX" or token.pos_ == "VERB" or token.pos_ == "ADJ":

            salida.writerow((cont, token.text,token.pos_))
            cont += 1



csvarchivo.close()
csvsalida.close()
'''
csvarchivo = open('entrada1000palabrasAPI.csv',encoding="utf8",errors='ignore')
entrada = csv.DictReader(csvarchivo,delimiter=";")


contSinonimos = 0
contRel = 0

for i in entrada:
    obj = requests.get('http://api.conceptnet.io/c/es/'+i['PALABRA']+'?offset=0&limit=100').json()
    for j in range (len(obj['edges'])):
        if obj['edges'][j]['rel']['label'] == 'Synonym' and obj['edges'][j]['end']['language'] == 'es' and obj['edges'][j]['start']['label'] == i['PALABRA']:
            print("Palabra a buscar:",i['PALABRA'],'SINÓNIMO:',obj['edges'][j]['end']['label'])
            contSinonimos += 1
        elif obj['edges'][j]['rel']['label'] == 'RelatedTo' and obj['edges'][j]['end']['language'] == 'es' and obj['edges'][j]['start']['label'] == i['PALABRA']:
            print("Palabra a buscar:",i['PALABRA'],"TÉRMINO RELACIONADO:", obj['edges'][j]['end']['label'])
            contRel += 1

print('SINONIMOS: ', contSinonimos)
print('TERMINOS RELACIONADOS: ', contRel)

csvarchivo.close()

import os
arrayContenidoDevuelto = []
arrayContenidoDevuelto = ["madrid"]

arraySinonimosFinal = []
encontrado = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csvarchivo = open(BASE_DIR + '/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')
archivo = csv.DictReader(csvarchivo, delimiter=";")

for i in range(len(arrayContenidoDevuelto)):
    for j in archivo:
        if arrayContenidoDevuelto[i] == j['PALABRA']:
            arraySinonimosFinal.append(j['PALABRA'])
            encontrado = True


for i in range(len(arraySinonimosFinal)):
    print(arraySinonimosFinal[i])






    #####   DEVUELVE TODOS LOS SINONIMOS Y TERMINOS RELACIONADOS DE LAS 1000 PALABRAS DE LA RAE

    def sinonimosPalabrasRAE():
        import os

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #csvarchivo = open('/Users/IRENE/git/TFG-1819-Analogias/PruebaPrototipo/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')
        #csvarchivo = open('C:/Users/Pablo/Documents/GitHub/TFG-1819-Analogias/PruebaPrototipo/prototipo/entrada1000palabrasAPI.csv', encoding="utf8", errors='ignore')
        csvarchivo = open(BASE_DIR+'/prototipo/entrada1000palabrasAPI.csv',encoding="utf8", errors='ignore')
        entrada = csv.DictReader(csvarchivo, delimiter=";")
        arraySalida = []
        for i in entrada:
            obj = requests.get('http://api.conceptnet.io/c/es/' + i['PALABRA'] + '?offset=0&limit=100').json()
            for j in range(len(obj['edges'])):
                if obj['edges'][j]['rel']['label'] == 'Synonym' and obj['edges'][j]['end']['language'] == 'es' and \
                        obj['edges'][j]['start']['label'] == i['PALABRA']:
                    arraySalida.append( "Palabra a buscar:" + i['PALABRA'] + "SINONIMO:" + obj['edges'][j]['end']['label'])
                elif obj['edges'][j]['rel']['label'] == 'RelatedTo' and obj['edges'][j]['end']['language'] == 'es' and \
                        obj['edges'][j]['start']['label'] == i['PALABRA']:
                    arraySalida.append("Palabra a buscar:" + i['PALABRA'] + "TÉRMINO RELACIONADO:" + obj['edges'][j]['end']['label'])

        csvarchivo.close()
        return arraySalida
    '''
#palabra = "gato"
#obj = requests.get('http://api.conceptnet.io/c/es/' + palabra + '?offset=0&limit=100').json()
#for i in range (len(obj['edges'])):
    #if obj['edges'][i]['rel']['label'] == 'Synonym':
        #print(obj['edges'][i])
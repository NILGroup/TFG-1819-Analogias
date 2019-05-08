import spacy
import csv
import requests


csvarchivo = open('palabrasHiperonimos.csv', 'r+',encoding="utf8", errors='ignore')
entrada = csv.DictReader(csvarchivo, delimiter=";")
contador = 0
for i in entrada:
    contador += int(i['VALIDOS'])
    print(contador)
salida = csv.writer(csvarchivo)
salida.writerow(('VALIDOS:', contador))
print(contador)

#CUENTA LAS PALABRAS GENERADAS TOTALES
'''
csvarchivo = open('palabrasHiperonimos.csv', 'r+',encoding="utf8", errors='ignore')
entrada = csv.DictReader(csvarchivo, delimiter=";")
contador = 0
lista = list()
for i in entrada:
    elem = i['HIPERONIMOS'].split(',')
    contador += len(elem)
salida = csv.writer(csvarchivo)
salida.writerow(('TOTAL:', contador))
print(contador)
'''
#TAGGEADOR DE PALABRAS FACILES
'''
nlp = spacy.load('es_core_news_sm')
frase = 'el coche es rojo'
frase = frase.split(" ")
for i in frase:
    doc = nlp(i)
    print(doc[0].text, doc[0].pos_)
'''
'''
csvarchivo = open('10000PALABRAS.csv', encoding="utf8", errors='ignore')
entrada = csv.reader(csvarchivo, delimiter=";")
csvsalida = open('10000PALABRASFILTRADAS.csv', 'w', encoding="utf8", newline="")
salida = csv.writer(csvsalida, delimiter=";")

salida.writerow(("NUMERO", "PALABRA", "TAG"))
cont = 1
for i in entrada:
    #print(i[1])
    doc = nlp(i[1])
    for token in doc:
        if token.pos_ == "ADV" or token.pos_ == "NOUN" or token.pos_ == "AUX" or token.pos_ == "VERB" or token.pos_ == "ADJ":

            salida.writerow((cont, token.text,token.pos_))
            cont += 1



csvarchivo.close()
csvsalida.close()
'''
'''
#ELIMINA PALABRAS REPETIDAS Y TAGGEA

nlp = spacy.load('es_core_news_md')

data = set()
cont = 1

csvarchivo = open('pruebaTecnologico.csv', encoding="utf8", errors='ignore')
entrada = csv.reader(csvarchivo, delimiter=";")
csvsalida = open('pruebaTecnologicoFiltrada.csv', 'w', encoding="utf8", newline="")
salida = csv.writer(csvsalida, delimiter=";")

salida.writerow(("NUMERO", "PALABRA", "TAG"))

for i in entrada:
    #print(i[0])
    data.add(i[0])

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
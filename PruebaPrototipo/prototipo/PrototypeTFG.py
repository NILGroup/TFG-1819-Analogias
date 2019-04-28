import spacy
import csv
import requests
import pandas as pd
import re
import os

#PARA QUE AL COMPARAR PALABRAS NO TENGA EN CUENTA LOS ACENTOS
from unidecode import unidecode







#os.makedirs('pictos',mode=0o777)
'''

#CREA FICHEROS CON SOLO LA PALABRA FACIL
csvarchivo = open('10000PALABRASFILTRADAS.csv', encoding="utf8", errors='ignore')
entrada = csv.DictReader(csvarchivo, delimiter=";")
csvsalida = open('10000_palabras_faciles.csv', 'w', encoding="utf8", newline="")
salida = csv.writer(csvsalida, delimiter=";")
for i in entrada:
    #print(i)
    salida.writerow([i['PALABRA']])

csvarchivo.close()
csvsalida.close()
'''
'''
#CLASIFICADOR DE PALABRAS SEGUN LETRA INICIAL

csvarchivo = open('5000PalabrasFiltradasYordenadas.csv', encoding="utf8", errors='ignore')
entrada = csv.DictReader(csvarchivo, delimiter=";")
for i in entrada:
    print(i['PALABRA'][0])
'''
'''
### FILTRO PARA BUSCAR CON REGEX    ###

csvarchivo = open('5000PalabrasFiltradasYordenadas.csv', encoding="utf8", errors='ignore')
entrada = csv.DictReader(csvarchivo, delimiter=";")

df = pd.DataFrame(list(entrada))
print(df)
filtro = df[df['PALABRA'] == 'abajo']
#filtro = df[df['PALABRA'].str.contains(r"^abajo/", regex=True)]

print(filtro)

'''
### ABRE EL ARCHIVO Y VUELVE A ESCRIBIR UNO NUEVO CON LAS PALABRAS ORDENADAS ALFABETICAMENTE ###
'''
with open('5000PalabrasFiltradas.csv',newline='', encoding='utf-8') as csvfile:
    entrada = csv.DictReader(csvfile, delimiter=";")
    sortedlist = sorted(entrada, key=lambda row:(row['PALABRA']), reverse=False)



csvsalida = open('5000PalabrasFiltradasYordenadas_V2.csv', 'w', encoding="utf8", newline='')
salida = csv.writer(csvsalida, delimiter=";")
salida.writerow(("NUMERO", "PALABRA", "ORDEN"))
###########################################################
'''
'''
#CREA UN CSV POR CADA INICIO DE PALABRA ORDENADA
csvarchivo = open('5000PalabrasFiltradasYordenadas.csv', encoding="utf8", errors='ignore')
entrada = csv.DictReader(csvarchivo, delimiter=";")


contador = 1
inicial = ''
for i in entrada:

    #print(csvsalida.seek())
    if inicial != i["PALABRA"][0]:
        csvsalida = open('indices/5000PalabrasFiltradasYordenadas_'+i["PALABRA"][0]+'.csv', 'w', encoding="utf8", newline='')
        salida = csv.writer(csvsalida, delimiter=";")
        print(i['PALABRA'])
        salida.writerow(('NUMERO',"PALABRA"))
        salida.writerow((contador,i['PALABRA']))
        inicial = i["PALABRA"][0]
    else:
        salida.writerow((contador, i['PALABRA']))
    contador += 1

#######
'''














'''
#OBTIENE GENERO Y NUMERO DE PALABRAS
obj = requests.get('https://holstein.fdi.ucm.es/nlp-api/analisis/coche',  verify=False).json()
print(obj['morfologico']['genero'])
print(obj['morfologico']['numero'])
'''
'''
doc = nlp("coche")

print(doc[0].pos_)
print(doc[0].tag_)
for token in doc:
    print(token.tag_, token.text)
    result_gender = re.match("NOUN__Gender=Masc", token.tag_)
    result_number = re.match("|Number=Sing", token.tag_)
    print(result_number)
    if result_gender != None:
        print("holaaaa")
    if result_number != None:
        print("adiooos")


'''

'''
#CLASIFICADOR SEMANTICO DE PALABRAS
nlp = spacy.load('es_core_news_md')

data = set()
cont = 1
csvarchivo = open('salida-definitiva.csv', encoding="utf8", errors='ignore')
entrada = csv.DictReader(csvarchivo, delimiter=";")
csvsalida = open('entrada1000palabrasAPI.csv', 'w', encoding="utf8")
salida = csv.writer(csvsalida, delimiter=";")

salida.writerow(("NUMERO", "PALABRA", "TAG"))

for i in entrada:
    data.add(i['PALABRA'])
cont = 1
for i in range(len(data)):
    doc = nlp(data[i])

    for token in doc:
        if token.pos_ == "ADV" or token.pos_ == "NOUN" or token.pos_ == "AUX" or token.pos_ == "VERB" or token.pos_ == "ADJ":

            salida.writerow((cont, token.text, token.pos_))
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

'''
palabra = "gato"
obj = requests.get('http://api.conceptnet.io/c/es/' + palabra + '?offset=0&limit=100').json()
for i in range (len(obj['edges'])):
    if obj['edges'][i]['rel']['label'] == 'Synonym':
        print(obj['edges'][i])

'''
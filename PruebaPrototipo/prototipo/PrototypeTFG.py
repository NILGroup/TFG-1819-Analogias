import spacy
import csv
import requests

nlp = spacy.load('es_core_news_sm')

data = []
cont = 1
'''
csvarchivo = open('salida-definitiva.csv', encoding="utf8", errors='ignore')
entrada = csv.DictReader(csvarchivo, delimiter=";")
csvsalida = open('entrada1000palabrasAPI.csv', 'w', encoding="utf8")
salida = csv.writer(csvsalida, delimiter=";")

salida.writerow(("NUMERO", "PALABRA", "TAG"))

for i in entrada:
    data.append(i['PALABRA'])
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
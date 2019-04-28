import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
import django
django.setup()
from django.db import connection
import csv


def binary(name):
    with open('pictos/'+name, 'rb') as file:
        binaryData = file.read()
    return binaryData

def pictogramas():
    files = os.listdir('pictos')
    for i in files:
        #print(i)
        id = i.rstrip('.png')
        img = binary(i)
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO pictogramas(id_picto,imagen) VALUES (%s, %s)', [id, img])
        #Pictos.objects.raw()

def datos_picto():
    csventrada = open('pictos.csv', encoding="utf8", errors='ignore')
    entrada = csv.DictReader(csventrada, delimiter=";")

    for i in entrada:
        palabra = i['PALABRA']
        offset31 = i['OFFSET3.1']
        offset30 = i['OFFSET3.0']
        id_picto = i['IDPICTO']
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO datos_picto(palabra,offset31, offset30, id_picto) VALUES (%s, %s,%s, %s)', [palabra, offset31,offset30, id_picto])



datos_picto()
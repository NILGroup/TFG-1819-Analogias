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

def pictos():

    csventrada = open('pictos.csv', encoding="utf8", errors='ignore')
    entrada = csv.DictReader(csventrada, delimiter=";")

    for i in entrada:
        palabra = i['PALABRA']
        #offset31 = i['OFFSET3.1']
        offset30 = i['OFFSET3.0']
        id_picto = i['IDPICTO']
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO pictos(offset30, palabra, id_picto) VALUES (%s, %s,%s)', [offset30, palabra, id_picto])

def prueba_cursor():
    '''
    offset30 = '5000'
    palabra = 'prueba'
    id_picto = '20'
    offset302 = '5001'
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO pictos(offset30, palabra, id_picto) VALUES (%s, %s,%s)', [offset30, palabra, id_picto])
        cursor.execute('INSERT INTO pictos(offset30, palabra, id_picto) VALUES (%s, %s,%s)', [offset302, palabra, id_picto])
        '''
    img = 'x091'
    with connection.cursor() as cursor:
        cursor.execute('UPDATE pictos SET imagen = %s WHERE id_picto=20',[img])

def inserta_pictos():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM datos_picto')
        rows = cursor.fetchall()
        #print(rows[0])
        for row in rows:
            cursor.execute('SELECT imagen FROM pictogramas WHERE id_picto = %s',[row[3]])
            img = cursor.fetchall()
            cursor.execute('UPDATE pictos SET imagen = %s WHERE id_picto= %s',[img, row[3]])
        cursor.execute('ALTER TABLE `pictos` CHANGE `imagen` `imagen` BLOB NOT NULL')
#datos_picto()
#pictos()
#prueba_cursor()
inserta_pictos()
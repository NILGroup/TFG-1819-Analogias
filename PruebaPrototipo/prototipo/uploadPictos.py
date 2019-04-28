import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
import django
django.setup()
from django.db import connection
import csv
import base64



def binary(name):
    with open('pictos/'+name, 'rb') as image:
        binaryData = base64.encodebytes(image.read())
        #print(binaryData)
        '''
        
        '''
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
    with connection.cursor() as cursor:
        cursor.execute('ALTER TABLE pictos CHANGE imagen imagen BLOB NOT NULL')
    '''
    offset30 = '5000'
    palabra = 'prueba'
    id_picto = '20'
    offset302 = '5001'
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO pictos(offset30, palabra, id_picto) VALUES (%s, %s,%s)', [offset30, palabra, id_picto])
        cursor.execute('INSERT INTO pictos(offset30, palabra, id_picto) VALUES (%s, %s,%s)', [offset302, palabra, id_picto])
        '''
    '''
    with connection.cursor() as cursor:
        cursor.execute('SELECT imagen FROM pictogramas WHERE id_picto = 2626')
        data= cursor.fetchall()
        #print(data[0][0])

        image_64_decode = base64.decodebytes(data[0][0])
        image_result = open('2239.png', 'wb')
        image_result.write(image_64_decode)
        image_result.close()
   '''


def inserta_pictos():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM datos_picto')
        rows = cursor.fetchall()
        #print(rows[0])
        for row in rows:
            cursor.execute('SELECT imagen FROM pictogramas WHERE id_picto = %s',[row[3]])
            img = cursor.fetchall()
            cursor.execute('UPDATE pictos SET imagen = %s WHERE id_picto= %s',[img, row[3]])

        cursor.execute('ALTER TABLE pictos CHANGE imagen imagen BLOB NOT NULL')
#datos_picto()
#pictos()
prueba_cursor()
#inserta_pictos()
#binary('2239.png')
#pictogramas()
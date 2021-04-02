'''Esto coge un cómic aleatorio de xkcd y descarga la imagen y el texto'''

# Esta librería es para intercambiar información con aplicaciones externas (API)

import requests # Documentación: https://2.python-requests.org/en/master/
import re
from random import randint

numero = randint(1, 2442)

# Información general
info = requests.get('https://xkcd.com/'+str(numero)+'/') # info es algo tomado del sitio web
print(info) # Supongo que esto es bueno (<Response [200]>)
# print(dir(info)) # Muestra la lista de atributos y métodos de info
# print(info.text) # Código html de la página


# Para encontrar el dibujo desde python:
contenido = info._content
# print(contenido) # Cadena de bytes (documento html)
imagenes = re.findall('https://(\S*).png',str(contenido)) # cuerpo es toda espresión regular comprendida entre <body> y </body> en la cadena equivalente a contenido
for imagen in imagenes: # Para ver cuántas hay
    imagen='https://'+imagen+'.png' #Devuelve el formato

imagen = requests.get(imagen)
# print(imagen) # (<Response [200]>)
# print(imagen.ok) # El sitio funciona bien (True)
# print(imagen.content) # Devuelve los bits de la imagen
dibujo=open('Comic.png', 'wb') # Abre 'Comic.png' con permiso 'wb' de escritura en bits
dibujo.write(imagen.content) # Escribe el contenido de la información en dibujo
dibujo.close()

# Texto
cuerpo = re.findall(r'<body>(.*?)</body>',str(contenido)) # cuerpo es toda espresión regular comprendida entre <body> y </body> en la cadena equivalente a contenido
# print(cuerpo) # Lista
# print(len(cuerpo)) # 1
secciones = re.findall(r'<div(.*?)</div>',cuerpo[0])
#print(len(secciones)) # 13

open('Dibujo.txt', 'w').write('')
archivo = open('Dibujo.txt', 'a')

for seccion in secciones:
    #print(seccion) # El texto descriptivo es la sección llamada "transcript"
    if re.compile('id="transcript"').search(seccion) != None: # Si a expresión regular contiene 'id="transcript"' en seccion...
        #print(seccion) # Cadena con la infromación de la sección transcripcción
        
        titulo = re.compile(r'{{(.*?)}}').search(seccion) # El título es la parte que venga entre dos llaves
        subtitulo = re.compile(r'\(\((.*?)\)\)').search(seccion)
        descripcion = re.compile(r'\[\[(.*?)\]\]').search(seccion)
        
        if titulo != None: # Si el título es no nulo...
            archivo.write(titulo.group().replace('{{','').replace('}}','')+'\n\n') # ... abre el documento de 'Dibujo.txt' y añade el título sin las llaves
        
        if subtitulo != None:
            archivo.write(subtitulo.group().replace('(','',1).replace(')','',1)+'\n\n')
        
        if descripcion != None:
            descripcion = descripcion.group().replace('\\n\\n','\n\n')
            archivo.write(descripcion.replace('[[','').replace(']]','')+'\n\n')
            # Hay cosas en cadenas de bytes que no me han apetecido cambiar como b'\xc3\xa2\xc2\x88\xc2\x9a2V' por ejemplo

archivo.close()
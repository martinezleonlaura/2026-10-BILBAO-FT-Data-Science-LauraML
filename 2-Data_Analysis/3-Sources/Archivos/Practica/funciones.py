import os
import shutil
from variables import *

def ordenar_archivos(ruta):

    #Guardo la ruta inicial, para después volver a ella
    ruta_inicial = os.getcwd()

    #Voy a la ruta que quiero oredenar
    os.chdir(ruta)

    #Hago un Try/Except para cuando estén ya las carpetas creadas no me de error
    for carpeta in carpetas_destino.keys():
        try:
            os.mkdir(carpeta)
        except FileExistsError:
            pass   #Si ya existe, simplemente continúa con la siguiente sin romperse

    lista_archivos = os.listdir() #Lo saco fuera para que no cambie en mitad del bucle

    #Recorro el diccionario
    for nombre_carpeta, extensiones in carpetas_destino.items():
        # Nos saltamos 'Otros' de momento, lo gestionamos al final
        if nombre_carpeta == 'Otros':
            continue

        #recorro las listas
        for extension in extensiones:
            for archivo in lista_archivos:
                if archivo.endswith(extension):
                    shutil.move(archivo, f"{nombre_carpeta}/")

    #Reviso la lista con lo que queda
    for archivo in os.listdir():
        if archivo not in carpetas_destino.keys():
            shutil.move(archivo, 'Otros/')


    resultado = os.walk(os.getcwd())

    #vuelvo a la ruta inicial 
    os.chdir(ruta_inicial)

    return [x for x in resultado]
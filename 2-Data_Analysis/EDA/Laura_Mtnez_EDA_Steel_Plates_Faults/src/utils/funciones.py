import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



#Fn aux para asignar la naturaleza de las vbles
def asignar_naturaleza(col, coordenadas, magnitud, intensidad, maq_mat, forma, defecto):
    if col in coordenadas: return 'Coordenadas y Ubicación Espacial (Geometría del Defecto)'
    elif col in magnitud: return 'Magnitud y Tamaño de la Falla'
    elif col in intensidad: return 'Intensidad y Luminosidad (Análisis Óptico)'
    elif col in maq_mat: return 'Características de la Maquinaria y Material'
    elif col in forma: return 'Índices de Forma y Complejidad (Morfología)'
    elif col in defecto: return 'Variables Objetivo (Clases de Defectos)'
    return 'No Clasificada'



#Fn aux para asignar una descripción de la naturaleza de la vble
def asignar_definicion(col, coordenadas, magnitud, intensidad, maq_mat, forma, defecto):
    if col in coordenadas: return 'Estas variables delimitan el "cuadro contenedor" (bounding box) del defecto en el plano de la lámina de acero.'
    elif col in magnitud: return 'Escala, área y tamaño logarítmico del defecto.'
    elif col in intensidad: return 'Indican cómo refleja la luz el defecto. Las fallas profundas o rugosas suelen alterar dramáticamente estos valores.'
    elif col in maq_mat: return 'Parámetros de configuración de la maquinaria y grosor/aleación del acero.'
    elif col in forma: return 'Variables continuas (de 0 a 1) calculadas por el sistema de visión artificial para entender la "silueta" de la imperfección.'
    return 'Variable objetivo para identificar el fallo real en la chapa.'



#Fn aux para comprobar si duplicados
def duplicados(dataframe):
    total_duplicados = dataframe.duplicated().sum()
    print(f"El número total de elementos duplicados es de: {total_duplicados}")



#Fn aux para comprobar si hay outliers
def detectar_outliers(dataframe, lista_columnas):
    
    resumen_outliers = []

    for col in lista_columnas:
        if col in dataframe.columns:
            Q1 = dataframe[col].quantile(0.25)
            Q3 = dataframe[col].quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - 1.5 * IQR
            limite_superior = Q3 + 1.5 * IQR
            
            conteo_outliers = ((dataframe[col] < limite_inferior) | (dataframe[col] > limite_superior)).sum()
            
            resumen_outliers.append({
                'Variable': col,
                'Mínimo': dataframe[col].min(),
                'Q1 (25%)': Q1,
                'Mediana (50%)': dataframe[col].median(),
                'Q3 (75%)': Q3,
                'Máximo': dataframe[col].max(),
                'Límite Superior (IQR)': limite_superior,
                'Cant. Outliers': conteo_outliers
            })
            
    return pd.DataFrame(resumen_outliers)



#Fn aux para asignar el tipo de acero
def asignar_tipo_acero(fila):
    if fila['TypeOfSteel_A300'] == 1:
            return "A300"
    elif fila['TypeOfSteel_A400'] == 1:
        return "A400"
    else:
        return "Otro / No Especificado"



#Fn aux para obtener el nombre del defecto
def asignar_tipo_defecto(fila, lista_defectos):
    for defecto in lista_defectos:
        if fila[defecto] == 1:
            return defecto
    return "Sin Defecto"



#Fn aux para agrupa espesores
def agrupar_espesores(espesor):
    if espesor <= 60:
        return "1 Fino (<= 60mm)"
    elif espesor <= 150:
        return "2 Medio (61mm - 150mm)"
    else:
        return "3 Grueso / Industrial (> 150mm)"



#Fn aux para análisis univariante



#Fn aux para análisis bivariante


#Fn aux para análisis multivariante/correlación mediante heatmap

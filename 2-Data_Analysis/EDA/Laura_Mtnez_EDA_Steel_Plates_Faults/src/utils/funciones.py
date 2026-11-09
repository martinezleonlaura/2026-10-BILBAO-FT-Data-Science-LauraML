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



#Fn aux para análisis UNIVARIANTE
def plot_porcentaje_defectos(dataframe, columna_defecto='Tipo_Defecto', color='royalblue'):
    plt.figure(figsize=(10, 5))
    #Calculo los porcentajes
    counts = dataframe[columna_defecto].value_counts()
    percentages = (counts / len(dataframe)) * 100
    #Creo el gráfico
    ax = sns.barplot(x=percentages.index, y=percentages.values, color='grey', edgecolor='black')
    plt.title("Impacto por Tipo de Defecto (% sobre el total de fallas)", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Tipo de Defecto", fontsize=12)
    plt.ylabel("Porcentaje (%)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, percentages.max() + 5)
    #Añado las etiquetas de porcentaje sobre cada barra
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%', 
                    (p.get_x() + p.get_width() / 2., p.get_height() + 0.5), 
                    ha='center', va='center', fontsize=10, fontweight='bold', color='black')           
    plt.tight_layout()
    plt.show()

def pareto_defectos(dataframe):
    #Filtro para quedarnos solo con los defectos identificables
    df_filtrado = dataframe[dataframe['Tipo_Defecto'] != 'Other_Faults']
    #Calculo frecuencias absolutas y porcentajes ordenados
    frecuencias = df_filtrado['Tipo_Defecto'].value_counts().to_frame()
    frecuencias.columns = ['Cantidad']
    frecuencias['Porcentaje'] = (frecuencias['Cantidad'] / frecuencias['Cantidad'].sum()) * 100
    frecuencias['Porcentaje_Acumulado'] = frecuencias['Porcentaje'].cumsum()
    #Configuro el lienzo principal (Barras)
    fig, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x=frecuencias.index, 
        y=frecuencias['Porcentaje'], 
        ax=ax1, 
        color='darkgrey', 
        edgecolor='black')
    ax1.set_title("Diagrama de Pareto: Foco Estratégico de Defectos Identificados", fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel("Tipo de Defecto", fontsize=12)
    ax1.set_ylabel("Porcentaje Individual (%)", fontsize=12)
    ax1.set_ylim(0, 110)
    ax1.tick_params(axis='x', rotation=30)
    #Añado los porcentajes individuales sobre cada barra
    for p in ax1.patches:
        ax1.annotate(f'{p.get_height():.1f}%', 
                    (p.get_x() + p.get_width() / 2., p.get_height() + 1.5), 
                    ha='center', va='center', fontsize=10, fontweight='bold')
    #Creo el segundo eje Y para la línea acumulada (Curva de Pareto)
    ax2 = ax1.twinx()
    ax2.plot(frecuencias.index, frecuencias['Porcentaje_Acumulado'], color='crimson', marker='o', linewidth=2, label='% Acumulado')
    ax2.set_ylabel("Porcentaje Acumulado (%)", fontsize=12)
    ax2.set_ylim(0, 110)
    #Añado los puntos numéricos del acumulado
    for i, txt in enumerate(frecuencias['Porcentaje_Acumulado']):
        ax2.annotate(f'{txt:.1f}%', (frecuencias.index[i], frecuencias['Porcentaje_Acumulado'].iloc[i] + 2),
                     color='crimson', weight='bold', ha='center', fontsize=9)
    #Dibujo la línea crítica del 80% (Ley de Pareto)
    ax2.axhline(80, color='red', linestyle='--', linewidth=1.5, alpha=0.8)
    ax2.text(0.5, 82, "Umbral Crítico de Pareto (80%)", color='red', fontsize=10, weight='bold')
    plt.tight_layout()
    plt.show()



#Fn aux para análisis BIVARIANTE
def acero_vs_defecto(dataframe, tipo_grafico='agrupado'):
    #Creo la tabla de contingencia SIN los márgenes 'All' para no alterar el gráfico
    tabla_cruce = pd.crosstab(dataframe['Tipo_Acero'], dataframe['Tipo_Defecto'])

    #Convierto los valores absolutos a porcentajes por cada Tipo de Acero (filas)
    # Esto equilibra la comparación ya que hay más placas A400 que A300
    tabla_porcentajes = tabla_cruce.div(tabla_cruce.sum(axis=1), axis=0) * 100
    #Configuro la figura
    fig, ax = plt.subplots(figsize=(12, 6))   
    if tipo_grafico == 'agrupado':
        # Barras agrupadas lado a lado
        tabla_porcentajes.plot(kind='bar', ax=ax, cmap='tab10', edgecolor='black', width=0.8)
        plt.ylabel("Porcentaje dentro del Tipo de Acero (%)", fontsize=12)   
    elif tipo_grafico == 'apilado':
        # Barras apiladas acumulando el 100%
        tabla_porcentajes.plot(kind='bar', stacked=True, ax=ax, cmap='tab10', edgecolor='black', width=0.6)
        plt.ylabel("Porcentaje Acumulado (%)", fontsize=12)   
    #Ajustes estéticos
    plt.title(f"Defectos vs Tipo de Acero", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Tipo de Acero", fontsize=12)
    plt.xticks(rotation=0)  # Mantiene las etiquetas A300 y A400 horizontales y legibles
    plt.ylim(0, 105)
    #Coloco la leyenda de los defectos fuera del gráfico para que no tape las barras
    plt.legend(title="Tipo de Defecto", bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def espesor_vs_defecto(dataframe, paleta="tab10"):
    #Creo la tabla cruzada sin incluir los totales/márgenes
    tabla_cruce = pd.crosstab(dataframe['Rango_Espesor'], dataframe['Tipo_Defecto'])
    #Normalizo al 100% dividiendo cada celda por el total de su fila
    tabla_proporcional = tabla_cruce.div(tabla_cruce.sum(axis=1), axis=0) * 100
    #Dibujo el gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    tabla_proporcional.plot(kind='barh', stacked=True, ax=ax, cmap=paleta, edgecolor='black', width=0.5)
    # Ajustes estéticos
    plt.title("Defectos según el Espesor de la Plancha", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Proporción del total de defectos en ese rango (%)", fontsize=12)
    plt.ylabel("Rango de Espesor", fontsize=12)
    plt.xlim(0, 100)
    #Posiciono la leyenda fuera del gráfico
    plt.legend(title="Tipo de Defecto", bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.grid(axis='x', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()



#Fn aux para análisis MULTIVARIANTE
def plot_plano_real_plancha(dataframe):
    plt.figure(figsize=(14, 6))
    #Calculo los centros nativos (Bounding Box)
    x_centro_nativo = (dataframe['X_Minimum'] + dataframe['X_Maximum']) / 2
    y_centro_nativo = (dataframe['Y_Minimum'] + dataframe['Y_Maximum']) / 2
    #Escalo a rango 0-1 usando los máximos absolutos del dataset
    x_normalizado = x_centro_nativo / dataframe['X_Maximum'].max()
    y_normalizado = y_centro_nativo / dataframe['Y_Maximum'].max()
    #Dimensiones comerciales siderúrgicas (en milímetros)
    ANCHO_REAL_MM = 1750
    LARGO_REAL_MM = 12000
    #INTERCAMBIO DE EJES PARA ORIENTACIÓN REAL DE LA LÍNEA:
    #El progreso a lo largo de la plancha (Largo) va en el eje Horizontal (X de la gráfica)
    #El ancho de la plancha va en el eje Vertical (Y de la gráfica)
    eje_horizontal_largo = y_normalizado * LARGO_REAL_MM
    eje_vertical_ancho = x_normalizado * ANCHO_REAL_MM
    #Dibujo el Scatter Plot emulando la geometría de la mesa de rodillos
    sns.scatterplot(
    data=dataframe,
    x=eje_horizontal_largo, 
    y=eje_vertical_ancho, 
    hue='Tipo_Defecto', 
    palette='tab10', 
    alpha=0.7, 
    edgecolor='none', 
    s=45) 
    #Ajusto títulos y etiquetas con las unidades y orientaciones del mundo real
    plt.title("Distribución Geométrica de Defectos en las Planchas", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Largo de la Plancha en la Línea de Avance (mm)", fontsize=12)
    plt.ylabel("Ancho de la Plancha (mm)", fontsize=12)
    #Establezco los límites físicos reales del material
    plt.xlim(-200, LARGO_REAL_MM + 200)
    plt.ylim(-50, ANCHO_REAL_MM + 50)
    #TRUCO INDUSTRIAL: Invierto el eje vertical del Ancho para que el "punto cero" 
    # de la cámara (arriba a la izquierda) coincida con la perspectiva real de inspección técnica
    plt.gca().invert_yaxis() 
    #Estética de plano de ingeniería
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend(title="Tipo de Defecto", bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

def plot_multivariante_heatmap(dataframe, lista_columnas):
    plt.figure(figsize=(12, 9))
    #Calculo la matriz de correlación para las variables seleccionadas
    matriz_corr = dataframe[lista_columnas].corr()
    #Dibujo el Heatmap
    sns.heatmap(matriz_corr, annot=True, fmt=".2f", cmap="coolwarm", 
                vmin=-1, vmax=1, linewidths=0.5, cbar=True)
    plt.title("Interacción entre Parámetros Físicos", 
              fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.show()



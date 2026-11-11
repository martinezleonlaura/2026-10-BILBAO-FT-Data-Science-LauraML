
# Optimización del Control de Calidad en Siderurgia mediante Ciencia de Datos

## Proyecto ralizado durante el Bootcamp Data Science & IA (The Bridge, Bilbao 2026)

---

## 1. Caso de Negocio e Impacto Financiero

Este proyecto implementa una solución proactiva basada en el resultado del análisis de datos recogido por una inspección Visión Artificial en una línea de laminación en caliente de placas gruesas de acero estructural de alta resistencia.

El retorno de inversión se calcula mediante la **Regla de Calidad 10X**, demostrando que el coste de subsanación de defectos se multiplica por diez en cada fase del flujo industrial:

* **Etapa 1 (Fábrica):** Coste base de 70 € por tonelada (el material bruto defectuoso se recicla inmediatamente).
* **Etapa 2 (Acabado):** Sube a 700 € por tonelada (pérdida de energía, mano de obra y horas de maquinaria; el material se convierte en chatarra/*scrap*).
* **Etapa 3 (Cliente Final):** Escala a 7.000 € por tonelada (debido a penalizaciones contractuales, logística inversa y daños reputacionales).

**Impacto:** La detección predictiva y temprana en la Fase 1 genera un **ahorro directo de 6.930 € por tonelada** frente a un escape de calidad al cliente final.

---

## 2. Estructura del Dataset

El dataset utilizado es **"Steel Plates Faults"**, recolectado por el *Semeion Research Center* (Roma) y financiado por el *Centro Sviluppo Materiali*. Consta de **1.941 registros y 34 variables** capturadas mediante cámaras ópticas industriales:

* **27 Variables Independientes:** Datos geométricos (coordenadas espaciales), magnitud de la falla (área en píxeles), análisis óptico (brillo, luminosidad) e índices morfológicos de la silueta del defecto.
* **7 Variables Dependientes (Clases de Defectos):** Pastry (Pliegue), Z_Scratch (Raya), K_Scratch (Surco), Stains (Mancha), Dirtiness (Suciedad), Bumps (Abolladura) y Other_Faults (Otro).

---

## 3. Hallazgos Clave y Validación Estadística

### A. El "Punto Ciego" del Software Actual (Análisis Univariante)

* **Insight:** El defecto genérico "Otro" representa el **34.7% del total de fallos**, disparándose hasta el **72.4% en los espesores gruesos** ($>150$ mm).
* **Validación Estadística:** Mediante un test de Chi-cuadrado de Pearson se demostró una dependencia absoluta entre el grosor y el fallo del software ($p\text{-valor} = 1.45 \times 10^{-177}$), confirmando un **sesgo sistemático (ceguera operativa)** en el algoritmo de clasificación actual.

### B. Dependencia del Defecto según la Aleación (Análisis Bivariante)

* **Insight:** Al aislar el ruido de la categoría "Otro", el Principio de Pareto demuestra que solo tres defectos (**Abolladura, Surco y Raya**) acumulan el **77.5% de las pérdidas reales** de la planta.
* **Distribución:** El acero blando (A300) es altamente vulnerable a deformaciones por impacto (**Abolladuras**), mientras que el acero duro de alta resistencia (A400) sufre de un desgaste abrasivo severo (**Surcos**) y problemas de lavado (**Manchas**).
* **Validación Estadística:** El test de Chi-cuadrado confirmó de manera contundente que la tipología del defecto mecánico real depende intrínsecamente de las propiedades físicas de la aleación ($p\text{-valor} = 1.47 \times 10^{-141}$).

### C. Distribución Anómala en Planta (Análisis Espacial)

Utilizando la función de simulación geométrica `plot_plano_real_plancha`, el **Test de Kolmogorov-Smirnov** demostró que los defectos no se distribuyen al azar ($p\text{-valor} \approx 0$):

* **Inestabilidad Transitoria (Largo - Eje X):** Los fallos se concentran masivamente en los **primeros 3 metros de la plancha** (fase de entrada/cabeza del lingote), estabilizándose el proceso en el cuerpo restante.
* **Fallo Mecánico Fijo (Ancho - Eje Y):** Se identificó una línea continua perfecta de defectos a lo largo de todo el eje longitudinal fija en la **coordenada de ~120 mm**, delatando un daño severo en un rodillo específico.

---

## 4. Plan de Acción (Estrategia Six Sigma)

### Bloque 1: Mantenimiento Mecánico

* **Intervención en los Rodillos (Eje Y):** Inspeccionar físicamente los rodillos de laminación en la coordenada exacta de 120 mm para eliminar la muesca o cuerpo extraño que raya el acero.
* **Estabilización de Cabeza (Eje X):** Ajustar la amortiguación hidráulica y las pinzas de arrastre al inicio de la marcha, además de precalentar homogéneamente el lingote para mitigar el impacto por choque térmico.

### Bloque 2: Calibración Inteligente por Aleación

* **Línea A300:** Amortiguar los picos de presión mecánica para evitar deformaciones físicas (Abolladuras y Pliegues).
* **Línea A400:** Instalar rodamientos rotativos en las guías laterales para suprimir la fricción abrasiva (Surcos) e incrementar la presión del agua en el descalillado hidráulico para eliminar las Manchas.

---

## 5. Productivización

Para desplegar la solución comercial (Fase II), se propone una **arquitectura de modelos en cascada segmentada por espesor:**

* **Planchas Finas $\le$ 60 mm:** Especializado en la detección microscópica de *Surcos* y *Manchas*.
* **Espesores Medios 61-150 mm:** Optimizado para las morfologías de *Abolladuras* y *Rayas*.
* **Bloques Gruesos $>$ 150 mm:** Modelo entrenado exclusivamente con imágenes de bloques industriales pesados para eliminar la ceguera algorítmica del software.
* **Monitoreo automatizado:** Si la tasa de defectos sin clasificar ("Otros") supera el 5%, el sistema enviará una alerta.

---

## 6. Estructura del Repositorio (src)

├── src /        

	└── data/

	│   └── steel-faults.csv       # Dataset original de inspección de acero

	├── notebooks/

	    └── pruebas_exploracion.ipynb   # Jupyter Notebook con el desarrollo de las pruebas iniciales

	├── utils/

	│   └── funciones.py           # Funciones de limpieza, outliers, test y gráficos

	└── main.ipynb          # Jupyter Notebook con el desarrollo analítico completo

├── Memoria.docx          # Memoria del Proyecto en Word

├── Memoria.pdf          # Memoria del Proyecto en PDF

├── Presentación.pptx          # Presentación de los Resultados en PowerPoint

└── README.md                  # Archivo README

---

## 7. Requisitos e Instalación

Para ejecutar el notebook y reproducir los análisis estadísticos de este proyecto, clona este repositorio e instala las librerías necesarias:

```bash
# Clonar el repositorio
git clone https://github.com
cd siderurgia-quality-control

# Instalar dependencias necesarias
pip install pandas numpy scipy matplotlib seaborn
```

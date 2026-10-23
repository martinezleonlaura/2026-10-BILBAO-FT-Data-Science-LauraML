from variables import DIMENSION, BARCOS, SIMBOLO_AGUA, SIMBOLO_BARCO, SIMBOLO_TOCADO, SIMBOLO_FALLO
import random
import pprint

class Tablero:

    #Atributos COMUNES
    dimension = DIMENSION

    #Atributos PROPIOS de cada Tablero
    def __init__(self, jugador:str, barcos: dict = BARCOS):
        self.jugador = jugador
        self.barcos = barcos
        #Cada tablero de cada jugador se compone de dos tableros: uno donde posiciona los barcos, y otro donde apunta los disparos
        self.tablero_barcos = [[SIMBOLO_AGUA for i in range(self.dimension)] for j in range(self.dimension)]
        self.tablero_disparos = [[SIMBOLO_AGUA for i in range(self.dimension)] for j in range(self.dimension)]
        self.coordenadas_barco = {}     #Para comprobar luego si he hundido el barco

    #Diferentes MÉTODOS para la clase Tablero
    def colocar_barcos_random(self):
        '''
        Método para elegir las coordenadas los barcos de manera aletoria y colocarlos.
        Dentro de este método llamo a otros métodos:
            1.- Para validar que la posición es corecta (no se sale del tablero, ni se solapa con otros barcos).
            2.- Una vez validada la posición, colocar el barco propiamente dicho.
        '''
        for nombre, eslora in self.barcos.items():
            colocado = False
            while not colocado:
                orientacion = random.choice(["N-S", "E-O"])
                x = random.randint(0, self.dimension - 1)
                y = random.randint(0, self.dimension - 1)
                if self.validar_posicion(orientacion, x, y, eslora):
                    self.colocar_barco_en_tablero(orientacion, x, y, eslora)
                    coordenadas_barco = []     #Guardo las coordenadas del barco para comprobar luego si lo he hundido
                    if orientacion == "E-O":
                        for i in range (y, y + eslora):
                            coordenadas_barco.append((x, i))
                    else:
                        for i in range (x, x + eslora):
                            coordenadas_barco.append((i, y))
                    self.coordenadas_barco[nombre] = coordenadas_barco      #Asigno la lista al diccionario
                    colocado = True


    def validar_posicion(self, orientacion:str, x: int, y: int, eslora: int):
        ''' 
        Método para validar una posición de un barco.
        En función de la orientación del barco compruebo:
            1.- Primero que no salga del tablero.
            2.- Segundo que no se solape con otros barcos, es decir que la celda está vacía (agua).
        '''
        if orientacion == "E-O":
            if y + eslora > self.dimension:  
                return False
            for i in range(y, y + eslora):      
                if self.tablero_barcos[x][i] != SIMBOLO_AGUA:
                    return False
        else:       #Es decir orientacion == "N-S"
            if x + eslora > self.dimension:
                return False
            for i in range (x, x + eslora):
                if self.tablero_barcos[i][y] != SIMBOLO_AGUA:
                    return False
        return True     #Si supera todos los "filtros"


    def colocar_barco_en_tablero(self, orientacion:str, x: int, y: int, eslora: int):
        ''' 
        Métodos para colocar un barco en el tablero.

        '''
        if orientacion == "E-O":
            for i in range (y, y + eslora):
                self.tablero_barcos[x][i] = SIMBOLO_BARCO
        else:
            for i in range (x, x + eslora):
                self.tablero_barcos[i][y] = SIMBOLO_BARCO


    def mostrar_tablero(self, solo_disparos=False):
        ''' 
        Método para mostrar el tablero de los barcos colocados en pantalla.
        '''
        if not solo_disparos:
            print()
            print(f"******TABLERO DE BARCOS DE {self.jugador.upper()}******")
            pprint.pprint(self.tablero_barcos)

        print()
        print(f"*****TABLERO DE DISPAROS*****")
        pprint.pprint(self.tablero_disparos)


    def disparo_coordenada(self, x: int, y: int):
        ''' 
        Método disparo coordenadas.Realizo varias comprobaciones:
            1.- Primero que la coordenada caiga dentro del tablero. Entero entre 0 y 9.
            2.- Segundo eue no haya disparado previamente a dicha posición.
            3.- Tercero si ha impactado a un barco.
            4.- Cuarto si ha impactado en agua.
        
        '''
        if not (0 <= x <= (self.dimension - 1) and 0 <= y <= (self.dimension - 1)):
            return "FIN", None
        if self.tablero_disparos[x][y] in [SIMBOLO_TOCADO, SIMBOLO_FALLO]:
            return "REPETIR", None
        
        if self.tablero_barcos[x][y] == SIMBOLO_BARCO:
            self.tablero_disparos[x][y] = SIMBOLO_TOCADO
            barco_afectado = None
            for barco, coordenadas in self.coordenadas_barco.items():
                if (x, y) in coordenadas:
                    coordenadas.remove((x, y))
                    barco_afectado = barco
                    break

            if barco_afectado and len(self.coordenadas_barco[barco_afectado]) == 0:
                return "HUNDIDO", barco_afectado
            
            else:
                return "TOCADO", None
        else:
            self.tablero_disparos[x][y] = SIMBOLO_FALLO
            return "AGUA", None


    def quedan_barcos(self):
        ''' 
        Método para comprobar si quedan barcos.
        Recorre el diccionario de barcos. 
        Mientras queden listas, el jugador no ha terminado con todos los barcos.
        '''
        for coordenadas in self.coordenadas_barco.values():
            if len(coordenadas) > 0:
                return True
        return False 


    def turno_maquina(tablero_jugador):
        while True:
            x = random.randint(0, DIMENSION - 1)
            y = random.randint(0, DIMENSION - 1)

            if tablero_jugador.tablero_barcos[x][y] == SIMBOLO_TOCADO or tablero_jugador.tablero_barcos[x][y] == SIMBOLO_FALLO:
                continue

            resultado, barco_afectado = tablero_jugador.disparo_coordenada(x,y)     
            return resultado, barco_afectado

    def solicitar_coordenada(self, elemento_coordenada: str):
        ''' 
        Método para pedir coordenada y comprobar que es un entero. x = fila, y = columna.
        Que este entre 0 y 9 (DIMENSION - 1) lo hace en otra parte del código.
        '''
        while True:
            try:
                valor = int(input(f"Introduzca {elemento_coordenada} (0-{self.dimension - 1})"))
                if 0 <= valor < self.dimension:
                    return valor
                print(f"La coordenada ({elemento_coordenada}) está fuera del tablero.")
            except ValueError:
                print("El valor introducido no es válido. Por favor, introduce un número entero.")
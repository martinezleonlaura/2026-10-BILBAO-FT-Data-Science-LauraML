from variables import DIMENSION


def iniciar_juego(): 
    ''' 
    Muestra el menú inicial y procesa la opción elegida por el usuario.
        Robustez:
            1.- En try/except compruebo que el usuario introduce un número entero (int)
            2.- Y con match/case si el número entero está entre 1 y 3
    '''
    while True:
        print (f"******BIENVENIDO A HUNDIR LA FLOTA******")
        try:
            opcion = int(input(f"Elige una opción. 1: Jugar, 2: Mostrar instruciones, 3: salir"))
        except ValueError:
            print(f"Por favor, introduzca un número entero válido (1: Jugar, 2: Mostrar instrucciones o 3: Salir)")
            continue

        match opcion:
            case 1:
                print()
                print(f"¡¡¡CORSARIO!!! Comienza la batalla...")
                return "JUGAR"

            case 2:
                print()
                print(f"Instrucciones:")
                print(f"Hay dos jugadores: tú y la máquina. Y un tablero de {DIMENSION}x{DIMENSION} posiciones donde irán los barcos")
                print(f"Lo primero que se hace es colocar los barcos de manera aleatoria.")
                print(f"4 barcos de 1 posición de eslora")
                print(f"3 barcos de 2 posiciones de eslora")
                print(f"2 barcos de 3 posiciones de eslora")
                print(f"1 barco de 4 posiciones de eslora")
                print(f"Tanto tú, como la máquina tenéis un tablero con barcos, y se trata de ir disparando y hundiendo los del adversario hasta que un jugador se queda sin barcos, y por tanto, pierde.")
                print(f"Funciona por turnos y empiezas tú.")
                print(f"En cada turno disparas a una coordenada (x,y) del tablero adversario. **Si aciertas, te vuelve a tocar**. En caso contrario, le toca a la máquina.")
                print(f"En los turnos de la máquina, si acierta también le vuelve a tocar.")
                print(f"Si se hunden todos los barcos de un jugador, el juego acaba y gana el otro.")

            case 3:
                print()
                print(f"Parece que hoy no tienes la energía suficiente :P. ¡¡¡LASTER ARTE!!!")
                return "SALIR"

            case _:
                (f"Opción incorrecta, introduzca un número entero válido (1: Jugar, 2: Mostrar instrucciones o 3: Salir)")


def solicitar_coordenada(self, elemento_coordenada: str):
    ''' 
    Método para pedir coordenada y comprobar que es un entero. x = fila, y = columna.
    Que este entre 0 y 9 (DIMENSION - 1) lo hace en otra parte del código.
    '''
    while True:
        try:
            valor = int(input(f"Introduzca {elemento_coordenada} (0-{self.dimension - 1})"))
            return valor
        except ValueError:
            print("El valor introducido no es válido. Por favor, introduce un número entero.")
 
 
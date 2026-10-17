import variables as variables
from clases import Tablero
import funciones as funciones

def jugar():
#Muestra el menú inicial def en la fn "iniciar_juego" uy procesa la opción elegida
    decision = funciones.iniciar_juego()
    if decision == "SALIR":
        return

#Si la opción elegida NO es "SALIR" crea los tableros
    nombre_usuario = input(f"Introduce tu nombre, corsario. En caso contrario, pulsa enter.")
    if not nombre_usuario:   
        nombre_usuario = "Usuario"
    
    tablero_humano = Tablero(jugador=nombre_usuario)
    tablero_maquina = Tablero(jugador="Máquina")


#Completa ambos tableros de manera alatoria con la fn "colocar_barcos_random"
    tablero_humano.colocar_barcos_random()
    tablero_maquina.colocar_barcos_random()

    print(f"Barcos colocados de manera aleatoria. ¡¡¡comienza la partida!!! GOOD LUCK!!!")
    tablero_humano.mostrar_tablero()

#Comienza la partida. COMIENZA EL USUARIO!!!
    while True:   
        turno_jugador = True
        
        while turno_jugador:
            print(f"Tu turno, {nombre_usuario}")
    #Solicita las coordenadas
            x = tablero_humano.solicitar_coordenada("Fila (x)")
            y = tablero_humano.solicitar_coordenada("Columna (y)")

    #Dispara sobre el tablero
            resultado = tablero_maquina.disparo_coordenada(x,y)

            match resultado:
                case "TOCADO":
                    print (f"¡¡¡TOCADO!!! Sigues jugando")

                case "HUNDIDO":
                    print (f"¡¡¡TOCADO y HUNDIDO!!!. Has hundido: {barco_afectado}")
                    if not tablero_maquina.quedan_barcos():
                        print(f"ZORIONAK!!! Con este, has hundido todos los barcos de tu adversario. YOU WIN!!!")
                        return      #Rompe el bucle while y se acaba la partida

                case "AGUA":
                    print(f"¡¡¡AGUA!!! Pierdes tu turno...")
                    turno_jugador = False

                case "REPETIR":
                    print(f"Ya habías disparado en esa posición, por favor, elige otra coordenada")
                    continue        #Bucle while, salta arriba y vuelve a empezar        

                case "FIN":
                    print(f"La coordenada elegida está fuera del tablero.")
                    continue        #Bucle while, salta arriba y vuelve a empezar

    #Turno de la MÁQUINA
        turno_maquina = True

        while turno_maquina:
            print(f"Turno de la máquina.")

            resultado = funciones.turno_maquina(tablero_humano)

            match resultado:
                case "TOCADO":
                    print (f"¡¡¡TOCADO!!!")

                case "HUNDIDO":
                    print (f"¡¡¡TOCADO y HUNDIDO!!! La máquina ha hundido {barco_afectado}")
                    if not tablero_humano.quedan_barcos():
                        print(f"Con este, la máquina ha hundido todos tus barcos. YOU LOSE!!!")
                        return      #Rompe el bucle while y se acaba la partida

                case "AGUA":
                    print(f"¡¡¡AGUA!!!")
                    turno_maquina = False

                case "REPETIR":
                    continue        #Bucle while, salta arriba y vuelve a empezar        

                case "FIN":
                    continue        #Bucle while, salta arriba y vuelve a empezar


if __name__ == "__main__":
    jugar()






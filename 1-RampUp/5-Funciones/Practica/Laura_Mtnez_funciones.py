def week_day(dia):
    dias_semana = {1: "Lunes",
               2: "Martes",
               3: "Miércoles",
               4: "Jueves",
               5: "Viernes",
               6: "Sábado",
               7: "Domingo"}
    if dia in dias_semana:
        return dias_semana[dia]
    else:
        return "Día erróneo"


def piramide(num_filas):
    for i in range(num_filas,0,-1):
        for j in range(i,0,-1):
            print (j,end=" ")
        print()


def comparar(x,y):
    if x == y:
        return ("Los números son iguales")
    elif x > y:
        return ("El primer número es mayor que el segundo")
    else:
        return ("El segundo número es mayor que el primero")


def contador(texto,letra_a_contar):
    conteo = 0
    for letra in texto.lower():
        if letra == letra_a_contar:
            conteo = conteo + 1
        else:
            conteo = conteo
    return conteo   


def conteo_letras(cadena):
    conteo_dict = {}
    for letra in cadena:
        if letra in conteo_dict:
            conteo_dict[letra] = conteo_dict[letra] + 1
        else:
            conteo_dict[letra] = 1
    return conteo_dict  


def add_or_remove (lista, comando, elemento = None):
    if comando == "add":
        lista.append(elemento)
        print(lista)
    elif comando == "remove":
        lista.remove(elemento)
        print(lista)
    else:
        print('Elige un comando correcto: "add" o "remove"') 


def unir(lista_palabras):
    frase = " ".join(lista_palabras)
    print(frase)


def fibonacci(num):
    if num == 0 or num == 1:
        return num
    else:
        return fibonacci(num - 1) + fibonacci(num - 2)


def area_cuadrado(base):
    return base ** 2


def area_triangulo(base, altura):
    return (base * altura) / 2


def area_circulo(radio):
    import math
    return math.pi * radio ** 2
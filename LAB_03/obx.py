import random

# Parámetros del algoritmo genético
tamaño_poblacion = 10
probabilidad_mutacion = 0.1
n_generaciones = 100

# Definir nodos y pesos de las aristas
nodos = ['G', 'A', 'B', 'R', 'I', 'E', 'L', 'P', 'C', 'O']
pesos = {}

for i in range(len(nodos)):
    for j in range(i + 1, len(nodos)):
        ciudad_actual = nodos[i]
        ciudad_siguiente = nodos[j]
        if ciudad_actual != ciudad_siguiente:
            peso = random.randint(1, 100)  # Peso aleatorio entre 1 y 100
            arista1 = (ciudad_actual, ciudad_siguiente)
            arista2 = (ciudad_siguiente, ciudad_actual)
            pesos[arista1] = peso
            pesos[arista2] = peso


# Funcion para calcular la aptitud de un individuo
def calcular_aptitud(individuo):
    aptitud = 0
    for i in range(len(individuo) - 1):
        ciudad_actual = individuo[i]
        ciudad_siguiente = individuo[i + 1]
        try:
            aptitud += pesos[(ciudad_actual, ciudad_siguiente)]
        except KeyError:
            # Si la arista no está presente en el diccionario de pesos, ignorarla
            continue
    # Sumar el peso de vuelta a la ciudad de origen
    try:
        aptitud += pesos[(individuo[-1], individuo[0])]
    except KeyError:
        # Si la arista no está presente en el diccionario de pesos, ignorarla
        pass
    return aptitud


# Generar poblacion inicial
poblacion = []
for _ in range(tamaño_poblacion):
    individuo = random.sample(nodos, len(nodos))
    poblacion.append(individuo)

# Guardar el resultado en un archivo de texto
with open('resultado.txt', 'w') as archivo:
    archivo.write("Poblacion Inicial:\n")
    for i, individuo in enumerate(poblacion, start=1):
        archivo.write(f"{i})\t{''.join(individuo)}\n")
    archivo.write("\n")

    # Comenzar las iteraciones
    for generacion in range(1, n_generaciones + 1):
        archivo.write(f"**** Iteracion {generacion} ****\n")
        
        # Calcular aptitud para cada individuo
        archivo.write("Calcular la Aptitud para cada Individuo:\n")
        for i, individuo in enumerate(poblacion, start=1):
            aptitud = calcular_aptitud(individuo)
            archivo.write(f"{i})\t{''.join(individuo)}\t{aptitud}\n")
        archivo.write("\n")

        # Crear Mating Pool (seleccion por ruleta)
        mating_pool = []
        aptitudes_relativas = []
        suma_aptitudes = sum(1 / calcular_aptitud(individuo) for individuo in poblacion)
        for individuo in poblacion:
            aptitud_relativa = (1 / calcular_aptitud(individuo)) / suma_aptitudes
            aptitudes_relativas.append(aptitud_relativa)
        for _ in range(tamaño_poblacion):
            r = random.random()
            suma = 0
            for i, aptitud_relativa in enumerate(aptitudes_relativas):
                suma += aptitud_relativa
                if suma >= r:
                    mating_pool.append(poblacion[i])
                    break

        # Selección de padres y cruzamiento (OBX)
        archivo.write("Seleccion de Padres\n")
        hijos = []
        for _ in range(tamaño_poblacion // 2):
            padre1 = random.choice(mating_pool)
            mating_pool.remove(padre1)
            padre2 = random.choice(mating_pool)
            mating_pool.remove(padre2)

            archivo.write(f"{''.join(padre1)} - {''.join(padre2)} => ")

            punto_corte1 = random.randint(1, len(nodos) - 1)
            punto_corte2 = random.randint(1, len(nodos) - 1)
            while punto_corte2 == punto_corte1:
                punto_corte2 = random.randint(1, len(nodos) - 1)
            if punto_corte2 < punto_corte1:
                punto_corte1, punto_corte2 = punto_corte2, punto_corte1

            hijo1 = padre1[:punto_corte1] + padre2[punto_corte1:punto_corte2] + padre1[punto_corte2:]
            hijo2 = padre2[:punto_corte1] + padre1[punto_corte1:punto_corte2] + padre2[punto_corte2:]
            hijos.append(hijo1)
            hijos.append(hijo2)

            archivo.write(f"{''.join(hijo1)} - {''.join(hijo2)}\n")


        # Mutacion (insercion de una letra)
        archivo.write("Mutacion:\n")
        for i, hijo in enumerate(hijos):
            if random.random() < probabilidad_mutacion:
                posicion = random.randint(0, len(nodos) - 1)
                nueva_letra = random.choice([nodo for nodo in nodos if nodo not in hijo])
                hijo_mutado = hijo[:posicion] + [nueva_letra] + hijo[posicion:]
                hijos[i] = hijo_mutado
                archivo.write(f"Posicion: {posicion} => {''.join(hijo)} - {''.join(hijo_mutado)}\n")
            else:
                archivo.write(f"Sin Mutacion: {i+1}\n")
        archivo.write("\n")


        # Reemplazar poblacion anterior con la descendencia
        poblacion = hijos

        # Eliminar individuos con nodos repetidos
        poblacion = [individuo for individuo in poblacion if len(set(individuo)) == len(individuo)]

        # Guardar la poblacion actual en el archivo de texto
        archivo.write("Nueva Poblacion:\n")
        for i, individuo in enumerate(poblacion, start=1):
            archivo.write(f"{i})\t{''.join(individuo)}\n")
        archivo.write("\n")

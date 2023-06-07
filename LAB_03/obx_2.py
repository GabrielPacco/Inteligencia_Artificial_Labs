import random

class AlgoritmoGenetico:
    def __init__(self, tamaño_poblacion, probabilidad_mutacion, n_generaciones, nodos):
        self.tamaño_poblacion = tamaño_poblacion
        self.probabilidad_mutacion = probabilidad_mutacion
        self.n_generaciones = n_generaciones
        self.nodos = nodos
        self.poblacion = []

    def generar_poblacion_inicial(self):
        for _ in range(self.tamaño_poblacion):
            individuo = random.sample(self.nodos, len(self.nodos))
            self.poblacion.append(individuo)

    def calcular_aptitud(self, individuo):
        aptitud = 0
        for i in range(len(individuo) - 1):
            nodo_actual = individuo[i]
            nodo_siguiente = individuo[i + 1]
            peso = pesos[(nodo_actual, nodo_siguiente)]
            aptitud += peso
        return aptitud

    def crear_mating_pool(self, aptitudes):
        mating_pool = []
        total_aptitudes = sum(aptitudes)
        probabilidades = [aptitud / total_aptitudes for aptitud in aptitudes]
        acumulador = 0
        for probabilidad in probabilidades:
            acumulador += probabilidad
            mating_pool.append(acumulador)
        return mating_pool

    def cruzamiento(self, padre1, padre2):
        hijo1 = [''] * len(padre1)
        hijo2 = [''] * len(padre2)
        puntos_corte = random.sample(range(1, len(padre1)), 2)
        puntos_corte.sort()
        punto_corte1, punto_corte2 = puntos_corte
        for i in range(punto_corte1, punto_corte2 + 1):
            hijo1[i] = padre1[i]
            hijo2[i] = padre2[i]
        idx_hijo1 = 0
        idx_hijo2 = 0
        for i in range(len(padre1)):
            if padre2[i] not in hijo1:
                while hijo1[idx_hijo1] != '':
                    idx_hijo1 += 1
                hijo1[idx_hijo1] = padre2[i]
            if padre1[i] not in hijo2:
                while hijo2[idx_hijo2] != '':
                    idx_hijo2 += 1
                hijo2[idx_hijo2] = padre1[i]
        return hijo1, hijo2

    def mutacion(self, individuo):
        if random.random() < self.probabilidad_mutacion:
            idx1 = random.randint(0, len(individuo) - 1)
            idx2 = random.randint(0, len(individuo) - 1)
            individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]

    def ejecutar_algoritmo_genetico(self):
        self.generar_poblacion_inicial()
        for generacion in range(self.n_generaciones):
            aptitudes = []
            for individuo in self.poblacion:
                aptitud = self.calcular_aptitud(individuo)
                aptitudes.append(aptitud)
            mating_pool = self.crear_mating_pool(aptitudes)
            nueva_generacion = []
            while len(nueva_generacion) < self.tamaño_poblacion:
                padre1 = random.choice(mating_pool)
                padre2 = random.choice(mating_pool)
                idx_padre1 = mating_pool.index(padre1)
                idx_padre2 = mating_pool.index(padre2)
                hijo1, hijo2 = self.cruzamiento(self.poblacion[idx_padre1], self.poblacion[idx_padre2])
                self.mutacion(hijo1)
                self.mutacion(hijo2)
                nueva_generacion.append(hijo1)
                if len(nueva_generacion) < self.tamaño_poblacion:
                    nueva_generacion.append(hijo2)
            self.poblacion = nueva_generacion
            self.guardar_iteracion(generacion)

    def guardar_iteracion(self, generacion):
        with open('resultado.txt', 'a') as archivo:
            archivo.write(f"\n**** Iteración {generacion + 1} ****\n")
            archivo.write("Creación de Mating Pool:\n")
            aptitudes = []
            for i, individuo in enumerate(self.poblacion, 1):
                aptitud = self.calcular_aptitud(individuo)
                aptitudes.append(aptitud)
                archivo.write(f"{aptitud}\t=>\t{i}\t=>\t{''.join(individuo)}\n")
            mating_pool = self.crear_mating_pool(aptitudes)
            archivo.write("\nSelección de Padres:\n")
            for _ in range(len(self.poblacion) // 2):
                idx_padre1 = mating_pool.index(random.choice(mating_pool))
                idx_padre2 = mating_pool.index(random.choice(mating_pool))
                archivo.write(f"{idx_padre1 + 1} - {idx_padre2 + 1} => ")
                archivo.write(f"{idx_padre1 // 2 + 1} - {idx_padre2 // 2 + 1} => ")
                archivo.write(f"{''.join(self.poblacion[idx_padre1])} - {''.join(self.poblacion[idx_padre2])}\n")
            archivo.write("\nCruzamiento:\n")
            for i in range(0, len(self.poblacion), 2):
                hijo1, hijo2 = self.cruzamiento(self.poblacion[i], self.poblacion[i + 1])
                archivo.write(f"{i + 1} {i + 2} => {i // 2 + 1} {i // 2 + 2}\n")
                archivo.write(f"{''.join(hijo1)} - {''.join(hijo2)}\n")
            archivo.write("\nMutación:\n")
            for i in range(len(self.poblacion)):
                self.mutacion(self.poblacion[i])
                archivo.write(f"Sin Mutación {i + 1}\n")
            archivo.write("\nNueva Población:\n")
            for i, individuo in enumerate(self.poblacion, 1):
                archivo.write(f"{i})\t{''.join(individuo)}\n")

nodos = list('GABRIELPCO')
pesos = {}
for i in range(len(nodos)):
    for j in range(i+1, len(nodos)):
        peso = random.randint(1, 20)
        pesos[(nodos[i], nodos[j])] = peso
        pesos[(nodos[j], nodos[i])] = peso

ga = AlgoritmoGenetico(tamaño_poblacion=10, probabilidad_mutacion=0.1, n_generaciones=100, nodos=nodos)
ga.ejecutar_algoritmo_genetico()

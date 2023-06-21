import numpy as np

# Datos de entrada
X = np.array([-5.193, 0.156, -8.661, 3.664, 29.499])
Y = np.array([-35.44, 13.888, -56.093, 53.798, 238.755])

# Parámetros del algoritmo de Gradiente Descendiente
intercepto_inicial = 10.75
pendiente_inicial = 20.35
tasa_aprendizaje = 0.001
num_iteraciones = 100

# Crear archivo de texto
with open('resultado.txt', 'w') as archivo:
    # Escribir los valores de los puntos
    archivo.write("X={" + ','.join(str(x) for x in X) + "}\n")
    archivo.write("Y={" + ','.join(str(y) for y in Y) + "}\n\n")

    # Escribir parámetros del algoritmo
    archivo.write("Gradiente Descendiente\n\n")
    archivo.write("Intercepto Inicial = {}\n".format(intercepto_inicial))
    archivo.write("Pendiente Inicial = {}\n".format(pendiente_inicial))
    archivo.write("Tasa de Aprendizaje = {}\n\n".format(tasa_aprendizaje))

    # Inicializar valores
    anterior_intercepto = intercepto_inicial
    anterior_pendiente = pendiente_inicial

    # Realizar iteraciones
    for i in range(1, num_iteraciones + 1):
        # Calcular derivadas
        derivada_intercepto = np.sum(2 * (anterior_intercepto + anterior_pendiente * X - Y))
        derivada_pendiente = np.sum(2 * X * (anterior_intercepto + anterior_pendiente * X - Y))

        # Actualizar valores
        nuevo_intercepto = anterior_intercepto - tasa_aprendizaje * derivada_intercepto
        nuevo_pendiente = anterior_pendiente - tasa_aprendizaje * derivada_pendiente

        # Escribir resultados en el archivo
        archivo.write("Iteración {}\n".format(i))
        archivo.write("Anterior Intercepto = {}\n".format(anterior_intercepto))
        archivo.write("Anterior Pendiente = {}\n".format(anterior_pendiente))
        archivo.write("Derivada Intercepto = {}\n".format(derivada_intercepto))
        archivo.write("Derivada Pendiente = {}\n".format(derivada_pendiente))
        archivo.write("Tasa de Aprendizaje = {}\n".format(tasa_aprendizaje))
        archivo.write("Nuevo Intercepto = {}\n".format(nuevo_intercepto))
        archivo.write("Nuevo Pendiente = {}\n\n".format(nuevo_pendiente))

        # Actualizar valores para la siguiente iteración
        anterior_intercepto = nuevo_intercepto
        anterior_pendiente = nuevo_pendiente

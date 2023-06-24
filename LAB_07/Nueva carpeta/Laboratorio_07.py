import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt

# Generar 50 puntos aleatorios
X, Y = datasets.make_regression(n_samples=50, n_features=1, noise=20)

# Parámetros del algoritmo de Gradiente Descendiente
intercepto_inicial = np.mean(Y)
pendiente_inicial = 0.0
tasa_aprendizaje = 0.001
num_iteraciones = 100

# Crear archivo de texto
with open('resultado.txt', 'w') as archivo:
    # Escribir los valores de los puntos
    archivo.write("X={" + ','.join(str(x) for x in np.squeeze(X)) + "}\n")
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
        archivo.write("Iteracion {}\n".format(i))
        archivo.write("Intercepto Anterior = {}\n".format(anterior_intercepto))
        archivo.write("Pendiente Anterior = {}\n".format(anterior_pendiente))
        archivo.write("Derivada del Intercepto = {}\n".format(derivada_intercepto))
        archivo.write("Derivada de la Pendiente = {}\n".format(derivada_pendiente))
        archivo.write("Tasa de Aprendizaje = {}\n".format(tasa_aprendizaje))
        archivo.write("Nuevo Intercepto = {}\n".format(nuevo_intercepto))
        archivo.write("Nueva Pendiente = {}\n\n".format(nuevo_pendiente))

        # Actualizar valores para la siguiente iteración
        anterior_intercepto = nuevo_intercepto
        anterior_pendiente = nuevo_pendiente


    # Calcular la pendiente y el intercepto
    X_mean = np.mean(X)
    Y_mean = np.mean(Y)
    num = 0
    denom = 0
    for i in range(len(X)):
        num += (X[i] - X_mean) * (Y[i] - Y_mean)
        denom += (X[i] - X_mean) ** 2
    pendiente = num / denom
    intercepto = Y_mean - pendiente * X_mean

    # Calcular los valores de la línea de regresión
    x_line = np.linspace(np.min(X), np.max(X), 100)
    y_line = intercepto + pendiente * x_line

    # Obtener el rango de los puntos generados
    x_range = np.max(X) - np.min(X)
    y_range = np.max(Y) - np.min(Y)

    # Calcular los límites de la gráfica para abarcar toda la nube de puntos
    x_min = np.min(X) - 0.1 * x_range
    x_max = np.max(X) + 0.1 * x_range
    y_min = np.min(Y) - 0.1 * y_range
    y_max = np.max(Y) + 0.1 * y_range

    # Graficar los puntos de la regresión lineal obtenida
    plt.scatter(X, Y, label='Puntos de datos')
    plt.plot(x_line, y_line, color='red', label='Regresión lineal')
    plt.title('Regresión Lineal')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(x_min, x_max)  # Ajustar los límites del eje X
    plt.ylim(y_min, y_max)  # Ajustar los límites del eje Y
    plt.legend()

    # Guardar la imagen en formato PNG
    plt.savefig('regresion_lineal.png')
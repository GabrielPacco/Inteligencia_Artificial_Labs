import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt

# Generar 100 puntos aleatorios en un espacio de dos dimensiones
puntos = np.random.rand(100, 2)

# Definir el número de clusters y el número de iteraciones
n_clusters = 3
n_iteraciones = 10

# Mejorar la inicialización de los centroides utilizando el algoritmo K-means++
kmeans_pp = KMeans(n_clusters=n_clusters, init='k-means++')
kmeans_pp.fit(puntos)
centroides = kmeans_pp.cluster_centers_

# Crear un DataFrame vacío para guardar los resultados de cada iteración
df_iteraciones = pd.DataFrame()

# Iterar n_iteraciones veces
for i in range(n_iteraciones):
    # Asignar cada punto al centroide más cercano
    indices = np.argmin(np.linalg.norm(puntos - centroides[:, np.newaxis], axis=2), axis=0)
    
    # Recalcular los centroides de los clusters
    centroides = np.array([np.mean(puntos[indices == j], axis=0) for j in range(n_clusters)])
    
    # Imprimir los centroides actualizados en cada iteración
    print(f'Centroides actualizados en la iteración {i}:')
    print(centroides)
    
    # Graficar los puntos y los centroides
    plt.scatter(puntos[:, 0], puntos[:, 1], c=indices)
    plt.scatter(centroides[:, 0], centroides[:, 1], c='red', marker='X')
    plt.title(f'Iteración {i}')
    plt.show()
    
    # Escribir los resultados de la iteración en el archivo de texto generado
    with open('distancias.txt', 'a') as f:
        f.write(f'Centroides actualizados en la iteración {i}:\n')
        f.write(f'{centroides}\n')
    
    # Agrupar los puntos en tres clusters
    kmeans = KMeans(n_clusters=n_clusters, init=centroides).fit(puntos)

    # Obtener las distancias de cada punto a cada centroide
    distancias = kmeans.transform(puntos)

    # Obtener los valores mínimos de cada fila
    minimos = np.min(distancias, axis=1)

    # Crear un DataFrame con las distancias y los valores mínimos
    df = pd.DataFrame({
        'ID': range(len(puntos)),
        'X': puntos[:, 0],
        'Y': puntos[:, 1],
        'Distancia C1': distancias[:, 0],
        'Distancia C2': distancias[:, 1],
        'Distancia C3': distancias[:, 2],
        'Min': minimos,
        'Número de Iteración': i
    })
    
    # Agregar los resultados de la iteración al DataFrame de iteraciones
    df_iteraciones = pd.concat([df_iteraciones, df])

# Escribir los resultados de todas las iteraciones en el archivo de texto generado
df_iteraciones.to_csv('distancias.txt', sep='\t', index=False, mode='a', line_terminator='\n')

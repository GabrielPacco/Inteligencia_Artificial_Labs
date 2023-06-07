import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt

def generar_puntos(num_puntos):
    puntos = np.random.randn(num_puntos, 2)
    return puntos

def realizar_kmeans(puntos, n_clusters, n_iteraciones):
    centroides = np.random.rand(n_clusters, 2)  # Generar centroides aleatorios
    kmeans = KMeans(n_clusters=n_clusters, init=centroides)
    
    df_iteraciones = pd.DataFrame()
    
    for i in range(n_iteraciones):
        kmeans.fit(puntos)  # Ajustar el modelo KMeans
        
        centroides = kmeans.cluster_centers_
        distancias = kmeans.transform(puntos)
        minimos = np.min(distancias, axis=1)
        
        print(f'Centroides actualizados en la iteración {i}:')
        print(np.round(centroides, decimals=4))
        
        plt.scatter(puntos[:, 0], puntos[:, 1], c=kmeans.labels_)
        plt.scatter(centroides[:, 0], centroides[:, 1], c='red', marker='X')
        plt.title(f'Iteración {i}')
        plt.show()
        
        df = pd.DataFrame({
            'ID': range(len(puntos)),
            'X': puntos[:, 0],
            '\t\t\t\tY': puntos[:, 1],
            '\t\t\t\tC1': np.round(distancias[:, 0], decimals=4),
            '\t\tC2': np.round(distancias[:, 1], decimals=4),
            '\t\tC3': np.round(distancias[:, 2], decimals=4),
            'Mínimo': np.round(minimos, decimals=4),
            'Número de Iteración': i
        })
        
        df_iteraciones = pd.concat([df_iteraciones, df])
    
    df_iteraciones.to_csv('distancias.txt', sep='\t', index=False)

# Generar 100 puntos aleatorios
puntos = generar_puntos(100)

# Definir el número de clusters y el número de iteraciones
n_clusters = 3
n_iteraciones = 10

realizar_kmeans(puntos, n_clusters, n_iteraciones)

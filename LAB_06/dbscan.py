import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import DBSCAN

# Generar conjunto de datos sintéticos
X, y = make_blobs(n_samples=100, centers=3, n_features=2)

# Definir parámetros del algoritmo
epsilon = 0.75
minPts = 2

# Aplicar algoritmo DBSCAN a los datos
dbscan = DBSCAN(eps=epsilon, min_samples=minPts)
dbscan.fit(X)

# Crear archivo de texto para escribir los resultados
with open('resultados.txt', 'w') as f:
    # Escribir los parámetros utilizados
    f.write(f'Parametros epsilon = {epsilon} \nminPts = {minPts}\n')
    
    # Escribir los puntos analizados
    f.write('Puntos analizados:\n')
    for i, punto in enumerate(X):
        f.write(f'{i+1}. ({punto[0]:.2f}, {punto[1]:.2f})\n')
    
    # Escribir los puntos no visitados
    f.write('\nPuntos no visitados: ')
    for i, label in enumerate(dbscan.labels_):
        if label == -1:
            f.write(f'{i+1}, ')
    f.write('\n')
    
    # Escribir los puntos visitados y los grupos generados
    grupos = set(dbscan.labels_)
    for grupo in grupos:
        if grupo == -1:
            continue
        f.write(f'Grupo {grupo}: ')
        for i, label in enumerate(dbscan.labels_):
            if label == grupo:
                f.write(f'{i+1}, ')
        f.write('\n')
    
    # Escribir las listas de vecinos
    f.write('Listas de vecinos:\n')
    for i, punto in enumerate(X):
        vecinos = dbscan.components_[np.intersect1d(np.where(dbscan.labels_ == dbscan.labels_[i]), np.arange(len(dbscan.components_)))]
        f.write(f'Punto {i+1}: ')
        for j, vecino in enumerate(vecinos):
            if np.array_equal(punto, vecino):
                continue
            f.write(f'{np.where(np.all(X == vecino, axis=1))[0][0]+1}, ')
        f.write('\n')
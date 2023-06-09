import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import DBSCAN

# Generar conjunto de datos sintéticos
X, y = make_blobs(n_samples=100, centers=3, n_features=2)

# Definir parámetros del algoritmo
epsilon = 0.50
minPts = 2

# Aplicar algoritmo DBSCAN a los datos
dbscan = DBSCAN(eps=epsilon, min_samples=minPts)
dbscan.fit(X)

# Crear archivo de texto para escribir los resultados
with open('resultados.txt', 'w') as f:
    # Escribir los parámetros utilizados
    f.write(f'Parametros\nepsilon = {epsilon}\nminPts = {minPts}\n')
    
    # Escribir los puntos analizados
    for i, punto in enumerate(X):
        f.write(f'{i+1}. ({punto[0]:.2f}, {punto[1]:.2f})\n')
    
    # Escribir los puntos no visitados
    f.write('\nPuntos no visitado: ')
    for i, label in enumerate(dbscan.labels_):
        if label == -1:
            f.write(f'{i+1}, ')
    f.write('\n')
    
    # Escribir los puntos visitados y los grupos generados
    grupos = set(dbscan.labels_)
    for grupo in grupos:
        if grupo == -1:
            continue
        f.write(f'Grupo {chr(grupo + 65)}: ')
        for i, label in enumerate(dbscan.labels_):
            if label == grupo:
                f.write(f'{i+1}, ')
        f.write('\n')
    
    # Escribir las listas de vecinos y actualizar los grupos
    for i, punto in enumerate(X):
        if dbscan.labels_[i] == -1:
            continue
        
        vecinos = dbscan.components_[np.intersect1d(np.where(dbscan.labels_ == dbscan.labels_[i]), np.arange(len(dbscan.components_)))]
        
        f.write(f'\nPunto visitado: {i+1}\nLista Vecinos: ')
        for j, vecino in enumerate(vecinos):
            if np.array_equal(punto, vecino):
                continue
            f.write(f'{np.where(np.all(X == vecino, axis=1))[0][0]+1}, ')
        
        auxiliar = []
        for j, vecino in enumerate(vecinos):
            if np.array_equal(punto, vecino):
                continue
            
            indice_vecino = np.where(np.all(X == vecino, axis=1))[0][0]
            vecinos_vecino = dbscan.components_[np.intersect1d(np.where(dbscan.labels_ == dbscan.labels_[indice_vecino]), np.arange(len(dbscan.components_)))]
            
            for k, vecino_vecino in enumerate(vecinos_vecino):
                indice_vecino_vecino = np.where(np.all(X == vecino_vecino, axis=1))[0][0]
                if indice_vecino_vecino not in auxiliar:
                    auxiliar.append(indice_vecino_vecino)
        
        f.write('\nLista Vecinos de Auxiliar: ')
        for j in auxiliar:
            f.write(f'{j+1}, ')
        
        grupo_actual = chr(dbscan.labels_[i] + 65)
        f.write(f'\nGrupo {grupo_actual}: ')
        for j in auxiliar:
            if dbscan.labels_[j] != dbscan.labels_[i]:
                dbscan.labels_[j] = dbscan.labels_[i]
            
            f.write(f'{j+1}, ')

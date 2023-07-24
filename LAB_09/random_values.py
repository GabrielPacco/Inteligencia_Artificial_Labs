import numpy as np

# Crear un array de números
numeros = np.array([5, 7, 2, 13, 4, 15, 9, 4, 6, 1,	3, 10, 4, 10, 8, 20, 18, 15, 20, 12, 6, 12, 13, 14, 10, 6, 21, 25])

# Crear un array con los valores 0.5 y -0.5
valores_aleatorios = np.array([0.5, -0.5])

# Seleccionar aleatoriamente un valor para cada elemento del array original
valores_seleccionados = np.random.choice(valores_aleatorios, size=numeros.shape)

# Sumar o restar los valores seleccionados a cada número del array
numeros_modificados = numeros + valores_seleccionados

# Mostrar el array modificado
print(numeros_modificados)



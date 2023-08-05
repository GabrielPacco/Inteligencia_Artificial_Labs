# Función de activación
def activation_function(x):
    if x > 0:
        return 1
    else:
        return 0

# Función para imprimir los pesos de forma bonita
def pretty_print_weights(weights):
    return [int(w) if w.is_integer() else round(w, 1) for w in weights]

# Conjunto de datos de entrenamiento
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [0, 0, 0, 1]

# Parámetros iniciales
weights = [0.2, 0.3, -0.1]  # w0 (bias), w1, w2
learning_rate = 0.1

# Abrir el archivo en modo escritura
with open("perceptron_output.txt", "w") as file:
    # Escribir los pesos iniciales
    file.write(f"Pesos iniciales: {pretty_print_weights(weights)}\n")

    # Realizar 7 épocas de entrenamiento
    for epoch in range(7):
        file.write(f"\nEpoca {epoch + 1}\n")

        # Iterar sobre cada punto de datos
        for i in range(len(X)):
            # Calcular la salida del perceptrón
            output = activation_function(weights[0] + weights[1]*X[i][0] + weights[2]*X[i][1])

            # Escribir el dato analizado, la salida esperada y la salida estimada
            file.write(f"Dato analizado: {X[i]}, Salida esperada: {y[i]}, Salida estimada: {output}\n")

            # Si la salida no coincide con la salida esperada, ajustar los pesos
            if output != y[i]:
                # Calcular el error
                error = y[i] - output

                # Escribir el valor del error
                file.write(f"Error: {error}\n")

                # Ajustar los pesos
                weights[0] = weights[0] + learning_rate * error
                weights[1] = weights[1] + learning_rate * error * X[i][0]
                weights[2] = weights[2] + learning_rate * error * X[i][1]

                # Escribir el valor de los nuevos pesos
                file.write(f"Nuevos pesos: {pretty_print_weights(weights)}\n")

print("Entrenamiento completado. Los resultados se han guardado en 'perceptron_output.txt'.")

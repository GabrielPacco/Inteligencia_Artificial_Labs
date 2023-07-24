import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def binary_cross_entropy(y_true, y_pred):
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return - (y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)).mean()

def gradient_descent(x, y, learning_rate, iterations):
    m = len(x)
    theta = np.zeros(2)
    
    for i in range(iterations):
        y_pred = sigmoid(np.dot(x, theta))
        error = binary_cross_entropy(y, y_pred)
        gradient = np.dot(x.T, (y_pred - y)) / m
        theta -= learning_rate * gradient
        if i % 1000 == 0:
            print(f"Iteracion {i+1}: Error = {error:.6f}")
    
    return theta

def predict(x, theta):
    return sigmoid(np.dot(x, theta))

# Datos de entrenamiento y test
x_train = np.array([5.5, 7.5, 12.5, 4.5, 15.5, 3.5, 5.5, 0.5, 3.5, 3.5, 9.5, 7.5, 17.5, 14.5, 19.5, 5.5, 11.5, 12.5, 13.5, 10.5, 20.5, 25.5])
y_train = np.array([0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1])
x_test = np.array([2.5, 8.5, 10.5, 19.5, 11.5, 6.5])
y_test = np.array([0, 1, 1, 1, 1, 0])

# Agregar columna de unos a los datos de entrenamiento para el intercepto
x_train_with_intercept = np.column_stack((np.ones(len(x_train)), x_train))

# Definir parámetros iniciales y entrenar el modelo
initial_learning_rate = 0.001
num_iterations = 100000
initial_theta = np.array([-0.9874, -2.1789])

final_theta = gradient_descent(x_train_with_intercept, y_train, initial_learning_rate, num_iterations)

# Generar puntos para la recta de Regresión Logística
x_plot = np.linspace(0, 26, 100)
y_plot = sigmoid(final_theta[0] + final_theta[1] * x_plot)

# Realizar predicciones en los datos de test
x_test_with_intercept = np.column_stack((np.ones(len(x_test)), x_test))
y_pred_test = predict(x_test_with_intercept, final_theta)

# Calcular el porcentaje de acierto en los datos de test
threshold = 0.5
y_pred_binary = (y_pred_test >= threshold).astype(int)
accuracy = (y_pred_binary == y_test).mean() * 100

# Generar el gráfico
plt.figure(figsize=(8, 6))
plt.scatter(x_train, y_train, color='blue', label='Datos de entrenamiento')
plt.scatter(x_test, y_test, color='red', label='Datos de test')
plt.plot(x_plot, y_plot, color='green', label='Regresión Logística')
plt.axhline(y=threshold, color='black', linestyle='--', label='Umbral')
plt.xlabel('Horas de Estudio')
plt.ylabel('Aprobado')
plt.title('Regresión Logística')
plt.legend()
plt.savefig('regresion_logistica.png')
plt.show()

# Generar el archivo .txt con los resultados
with open("resultados.txt", "w") as file:
    file.write("Gabriel Pacco Huaraca\n")
    file.write(f"Pendiente anterior = {initial_theta[0]:.4f}\n")
    file.write(f"Intercepto anterior = {initial_theta[1]:.4f}\n")
    file.write(f"Tasa de aprendizaje = {initial_learning_rate}\n")
    file.write(f"Cantidad de Iteraciones = {num_iterations}\n")
    file.write(f"Umbral = {threshold}\n")
    file.write("Datos de Entrenamiento:\n")
    file.write(f"x = {x_train.tolist()}\n")
    file.write(f"y = {y_train.tolist()}\n")
    file.write("Datos de Test:\n")
    file.write(f"x = {x_test.tolist()}\n")
    file.write(f"y = {y_test.tolist()}\n\n")
    
    for i in range(num_iterations):
        y_pred_train = predict(x_train_with_intercept, initial_theta)
        error = binary_cross_entropy(y_train, y_pred_train)
        gradient = np.dot(x_train_with_intercept.T, (y_pred_train - y_train)) / len(x_train)
        new_theta = initial_theta - initial_learning_rate * gradient
        file.write(f"Iteracion {i+1}\n")
        file.write(f"Pendiente anterior = {initial_theta[0]:.4f}\n")
        file.write(f"Intercepto anterior = {initial_theta[1]:.4f}\n")
        file.write(f"Error = {error:.6f}\n")
        file.write(f"Tasa de aprendizaje = {initial_learning_rate}\n")
        file.write(f"Derivada pendiente = {gradient[1]:.6f}\n")
        file.write(f"Derivada intercepto = {gradient[0]:.6f}\n")
        file.write(f"Pendiente nueva = {new_theta[0]:.4f}\n")
        file.write(f"Intercepto nuevo = {new_theta[1]:.4f}\n\n")
        initial_theta = new_theta
    
    file.write("Test\n")
    for i in range(len(x_test)):
        y_prob = predict(np.array([1, x_test[i]]), final_theta)
        y_pred = 1 if y_prob >= threshold else 0
        file.write(f"Primer dato {x_test[i]} = {y_prob}, aprobado estimado = {y_pred}, ")
        if y_pred == y_test[i]:
            file.write("Correcto\n")
        else:
            file.write("Incorrecto\n")
    file.write(f"Porcentaje de Acierto: {accuracy:.2f}%\n")


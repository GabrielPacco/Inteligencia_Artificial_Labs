import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

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

def gradient_descent(x, y, learning_rate, iterations):
    m = len(x)
    theta = np.zeros(2)
    
    for i in range(iterations):
        y_pred = sigmoid(np.dot(x, theta))
        gradient = np.dot(x.T, (y_pred - y)) / m
        theta -= learning_rate * gradient
    
    return theta

final_theta = gradient_descent(x_train_with_intercept, y_train, initial_learning_rate, num_iterations)

# Generar puntos para la recta de Regresión Logística
x_plot = np.linspace(0, 26, 100)
y_plot = sigmoid(final_theta[0] + final_theta[1] * x_plot)

# Realizar predicciones en los datos de test
x_test_with_intercept = np.column_stack((np.ones(len(x_test)), x_test))
y_pred_test = sigmoid(np.dot(x_test_with_intercept, final_theta))

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

# Imprimir porcentaje de acierto
print(f"Porcentaje de Acierto: {accuracy:.2f}%")

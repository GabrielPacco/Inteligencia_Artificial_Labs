import pandas as pd
from math import log2
from sklearn.metrics import accuracy_score

# Clase para representar un nodo del árbol de decisión
class Node:
    def __init__(self, attribute, children):
        self.attribute = attribute
        self.children = children

# Función para calcular la entropía de un conjunto de datos
def entropy(data):
    class_counts = data['disease_Covid-19'].value_counts()
    total_instances = len(data)
    entropy = 0
    for count in class_counts:
        probability = count / total_instances
        entropy -= probability * log2(probability)
    return entropy

# Función para calcular la ganancia de información de un atributo
def information_gain(data, attribute):
    total_entropy = entropy(data)
    attribute_values = data[attribute].unique()
    weighted_entropy = 0
    for value in attribute_values:
        subset = data[data[attribute] == value]
        subset_entropy = entropy(subset)
        subset_probability = len(subset) / len(data)
        weighted_entropy += subset_probability * subset_entropy
    return total_entropy - weighted_entropy

# Función para seleccionar el mejor atributo para dividir el conjunto de datos
def select_best_attribute(data):
    attributes = data.columns.drop('disease_Covid-19')
    best_attribute = None
    best_gain = -1
    for attribute in attributes:
        gain = information_gain(data, attribute)
        if gain > best_gain:
            best_gain = gain
            best_attribute = attribute
    return best_attribute

def build_tree(data):
    if len(data['disease_Covid-19'].unique()) == 1:
        return data['disease_Covid-19'].iloc[0]

    if len(data.columns) == 1:
        return data['disease_Covid-19'].mode().iloc[0]

    best_attribute = select_best_attribute(data)
    tree = Node(best_attribute, {})

    values = data[best_attribute].unique()
    for value in values:
        subset = data[data[best_attribute] == value]
        if len(subset) == 0:  # Si no hay datos en el subconjunto, devolver la clase más común en todo el conjunto
            tree.children[value] = data['disease_Covid-19'].mode().iloc[0]
        else:
            tree.children[value] = build_tree(subset.drop(columns=[best_attribute]))

    return tree


# Función para construir el árbol de decisión y mostrar la ganancia de información en cada paso
def build_tree_with_gain_logging(data, file):
    if len(data['disease_Covid-19'].unique()) == 1:
        return data['disease_Covid-19'].iloc[0]

    # Calcula la ganancia de información para cada atributo en cada paso
    attributes = data.columns.drop('disease_Covid-19')
    for attribute in attributes:
        gain = information_gain(data, attribute)
        file.write(f"{attribute}: {gain:.4f}\n")

    best_attribute = select_best_attribute(data)
    tree = Node(best_attribute, {})

    values = data[best_attribute].unique()
    for value in values:
        subset = data[data[best_attribute] == value]
        if len(subset) == 0:  # Si no hay datos en el subconjunto, devolver la clase más común en todo el conjunto
            tree.children[value] = data['disease_Covid-19'].mode().iloc[0]
        else:
            tree.children[value] = build_tree_with_gain_logging(subset.drop(columns=[best_attribute]), file)

    return tree


# Función para realizar predicciones con el árbol de decisión
def predict(tree, instance):
    if isinstance(tree, str):
        return tree

    attribute = tree.attribute
    value = instance.get(attribute)  # Usar get() para obtener el valor del atributo, para manejar atributos no vistos

    if value in tree.children:
        return predict(tree.children[value], instance)
    else:
        # Si el valor no se encuentra en los hijos del nodo, ir a la clase más común de ese nodo
        class_counts = [tree.children[child] for child in tree.children]
        predicted_class = max(set(class_counts), key=class_counts.count)
        return predicted_class

# Paso 1: Cargar los datos de entrenamiento y prueba
train_data = pd.read_csv("virus_train.csv")
test_data = pd.read_csv("virus_test.csv")

# Convertir los valores "yes" y "no" en valores binarios 1 y 0
binary_labels = {"yes": 1, "no": 0}
train_data["fever"] = train_data["fever"].map(binary_labels)
train_data["cough"] = train_data["cough"].map(binary_labels)
test_data["fever"] = test_data["fever"].map(binary_labels)
test_data["cough"] = test_data["cough"].map(binary_labels)

# Codificar las columnas categóricas usando one-hot encoding
train_data = pd.get_dummies(train_data, columns=["fatigue", "pain", "disease"])
test_data = pd.get_dummies(test_data, columns=["fatigue", "pain", "disease"])

# Ajustar las columnas en el conjunto de prueba para que coincidan con el conjunto de entrenamiento
# Asegurarse de que todas las columnas presentes en el conjunto de entrenamiento también estén en el conjunto de prueba
missing_cols = set(train_data.columns) - set(test_data.columns)
for col in missing_cols:
    test_data[col] = 0

# Ordenar las columnas para que tengan el mismo orden en ambos conjuntos de datos
test_data = test_data[train_data.columns]

# Separar características (atributos) y etiquetas de clase
X_train = train_data.drop("disease_Covid-19", axis=1)  # Características de entrenamiento
y_train = train_data["disease_Covid-19"]  # Etiquetas de clase de entrenamiento
X_test = test_data.drop("disease_Covid-19", axis=1)  # Características de prueba
y_test = test_data["disease_Covid-19"]  # Etiquetas de clase de prueba

# Paso 2: Crear el árbol de decisión con el algoritmo ID3 y entrenarlo
tree = build_tree(pd.concat([X_train, y_train], axis=1))

# Paso 3: Realizar predicciones sobre los datos de prueba
# Rellenar los valores faltantes en X_test con la moda de cada columna
X_test_filled = X_test.fillna(X_train.mode().iloc[0])

predicted_diseases = X_test_filled.apply(lambda instance: predict(tree, instance), axis=1)

# Paso 4: Calcular la tasa de acierto del modelo
accuracy = accuracy_score(y_test, predicted_diseases)


# Paso 5: Calcular la ganancia de información en cada paso y generar el archivo "informe_arbol_decision.txt"
with open("informe_arbol_decision.txt", "w") as file:
    # Información básica
    file.write("Nombre del alumno: [Gabriel Pacco Huaraca]\n")
    file.write("Algoritmo utilizado: ID3\n")
    file.write("Conjunto de entrenamiento: virus_train.csv\n")
    file.write("Conjunto de prueba: virus_test.csv\n\n")

    # Ganancia de información en cada paso
    file.write("Ganancia de informacion en cada paso:\n")
    build_tree_with_gain_logging(pd.concat([X_train, y_train], axis=1), file)

    file.write("\n")

    # Predicciones para cada elemento del conjunto de prueba
    file.write("Predicciones para cada elemento del conjunto de prueba:\n")
    for i, (features, true_label, predicted_label) in enumerate(zip(X_test_filled.values, y_test, predicted_diseases)):
        features_str = ", ".join([f"{col}={val}" for col, val in zip(X_test_filled.columns, features)])
        true_class_name = str(true_label)
        predicted_class_name = str(predicted_label)
        file.write(f"Instancia {i + 1}: {features_str}, Clase real: {true_class_name}, Clase pronosticada: {predicted_class_name}\n")
    file.write("\n")
    
    # Tasa de acierto del árbol de decisión
    file.write(f"Tasa de acierto del arbol de decision: {accuracy:.2f}\n")


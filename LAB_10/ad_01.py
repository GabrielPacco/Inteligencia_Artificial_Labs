import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from io import StringIO
import pydotplus
from IPython.display import Image

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

# Paso 2: Crear el modelo de árbol de decisión con el algoritmo ID3 y entrenarlo
model = DecisionTreeClassifier(criterion="entropy")
model.fit(X_train, y_train)

# Paso 3: Realizar predicciones sobre los datos de prueba
predicted_diseases = model.predict(X_test)

# Codificar las etiquetas de clase usando LabelEncoder
le = LabelEncoder()
y_test_encoded = le.fit_transform(y_test)
predicted_diseases_encoded = le.transform(predicted_diseases)

# Paso 4: Calcular la tasa de acierto del modelo
accuracy = accuracy_score(y_test_encoded, predicted_diseases_encoded)

# Paso 5: Generar el archivo .txt con la información solicitada
with open("informe_arbol_decision.txt", "w") as file:
    # Información básica
    file.write("Nombre del alumno: [Tu Nombre]\n")
    file.write("Algoritmo utilizado: ID3\n")
    file.write("Conjunto de entrenamiento: virus_train.csv\n")
    file.write("Conjunto de prueba: virus_test.csv\n\n")
    
    # Ganancia de información en cada paso
    file.write("Ganancia de información en cada paso:\n")
    tree_structure = StringIO()
    tree_structure = model.tree_
    
    def print_node_info(node, depth):
        indent = "  " * depth
        if tree_structure.feature[node] != -2:
            feature_name = X_train.columns[tree_structure.feature[node]]
            file.write(f"{indent}- Nodo {node} (atributo '{feature_name}')\n")
            file.write(f"{indent}  Ganancia de información: {tree_structure.impurity[node] - tree_structure.weighted_n_node_samples[node] / tree_structure.weighted_n_node_samples[0] * tree_structure.impurity[tree_structure.children_left[node]] - tree_structure.weighted_n_node_samples[node] / tree_structure.weighted_n_node_samples[0] * tree_structure.impurity[tree_structure.children_right[node]]:.4f}\n")
            print_node_info(tree_structure.children_left[node], depth + 1)
            print_node_info(tree_structure.children_right[node], depth + 1)
        else:
            class_name = le.classes_[tree_structure.value[node][0].argmax()]
            file.write(f"{indent}- Nodo {node} (hoja, clase '{class_name}')\n")
    
    print_node_info(0, 0)
    file.write("\n")
    
    # Predicciones para cada elemento del conjunto de prueba
    file.write("Predicciones para cada elemento del conjunto de prueba:\n")
    for i, (features, true_label, predicted_label) in enumerate(zip(X_test.values, y_test, predicted_diseases)):
        features_str = ", ".join([f"{col}={val}" for col, val in zip(X_test.columns, features)])
        true_class_name = le.classes_[true_label]
        predicted_class_name = le.classes_[predicted_label]
        file.write(f"Instancia {i + 1}: {features_str}, Clase real: {true_class_name}, Clase pronosticada: {predicted_class_name}\n")
    file.write("\n")
    
    # Tasa de acierto del árbol de decisión
    file.write(f"Tasa de acierto del árbol de decisión: {accuracy:.2f}\n")

# Paso 6: Generar una imagen en formato .png del árbol de decisión generado
dot_data = StringIO()
export_graphviz(
    model,
    out_file=dot_data,
    feature_names=X_train.columns,
    class_names=["SARS-CoV1", "Covid-19"],  # Especificar los nombres de las clases para una mejor visualización
    filled=True,
    rounded=True,
    special_characters=True
)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png("arbol_decision.png")

# Mostrar la imagen del árbol de decisión generado
Image(graph.create_png())
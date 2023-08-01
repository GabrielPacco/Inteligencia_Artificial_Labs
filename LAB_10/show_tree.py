import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.preprocessing import LabelEncoder
from io import StringIO
import pydotplus

# Paso 1: Cargar los datos de entrenamiento
train_data = pd.read_csv("virus_train.csv")

# Convertir los valores "yes" y "no" en valores binarios 1 y 0
binary_labels = {"yes": 1, "no": 0}
train_data["fever"] = train_data["fever"].map(binary_labels)
train_data["cough"] = train_data["cough"].map(binary_labels)

# Codificar las columnas categóricas usando one-hot encoding
train_data = pd.get_dummies(train_data, columns=["fatigue", "pain", "disease"])

# Separar características (atributos) y etiquetas de clase
X_train = train_data.drop("disease_Covid-19", axis=1)  # Características de entrenamiento
y_train = train_data["disease_Covid-19"]  # Etiquetas de clase de entrenamiento

# Paso 2: Crear el modelo de árbol de decisión con el algoritmo ID3 y entrenarlo
model = DecisionTreeClassifier(criterion="entropy")
model.fit(X_train, y_train)

# Paso 3: Generar el archivo .txt con la información solicitada
with open("informe_arbol_decision.txt", "w") as file:
    # Información básica
    file.write("Nombre del alumno: [Tu Nombre]\n")
    file.write("Algoritmo utilizado: ID3\n")
    file.write("Conjunto de entrenamiento: virus_train.csv\n\n")
    
    # Ganancia de información en cada paso
    file.write("Ganancia de información en cada paso:\n")
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
            class_name = model.classes_[tree_structure.value[node][0].argmax()]
            file.write(f"{indent}- Nodo {node} (hoja, clase '{class_name}')\n")
    
    print_node_info(0, 0)
    file.write("\n")
    
    # Tasa de acierto del árbol de decisión en el conjunto de entrenamiento
    accuracy = model.score(X_train, y_train)
    file.write(f"Tasa de acierto del árbol de decisión en el conjunto de entrenamiento: {accuracy:.2f}\n")

# Paso 4: Generar una imagen en formato .png del árbol de decisión generado
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

print("Árbol de decisión generado y guardado en 'arbol_decision.png'.")

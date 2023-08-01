
def obx(parent1, parent2, indices):
    """
    Cruce OBX entre dos padres, intercambiando los elementos en las posiciones dadas por la lista de índices.
    """
    size = len(parent1)
    child = [None] * size
    for i in indices:
        child[i] = parent1[i]
    j = 0
    for i in range(size):
        if child[i] is None:
            while parent2[j] in child:
                j += 1
            child[i] = parent2[j]
            j += 1
    return child

parent1 = ['A', 'B', 'C', 'D', 'F', 'E', 'G']
parent2 = ['C', 'E', 'G', 'A', 'D', 'F', 'B'] 
indices = [1, 3, 4]

child1 = obx(parent1, parent2, indices)
child2 = obx(parent2, parent1, indices)

print("Padre 1:", parent1)
print("Padre 2:", parent2)
print("Hijo 1 OBX:", child1)
print("Hijo 2 OBX:", child2)
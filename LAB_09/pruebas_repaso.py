import random

def pbx(parent1, parent2, indices):
    """
    Cruce PBX entre dos padres, intercambiando los elementos en las posiciones dadas por la lista de índices.
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
    return child

def obx(parent1, parent2, indices):
    """
    Cruce OBX entre dos padres, intercambiando los elementos en las posiciones dadas por la lista de índices.
    """
    size = len(parent1)
    child = [None] * size
    for i in indices:
        child[i] = parent1[i]
    for i in range(size):
        if child[i] is None:
            options = [parent2[j] for j in range(size) if parent2[j] not in child]
            child[i] = random.choice(options)
    return child

parent1 = ['A', 'B', 'C', 'D', 'F', 'E', 'G']
parent2 = ['C', 'E', 'G', 'A', 'D', 'F', 'B'] 

child_pbx = pbx(parent1, parent2, [1, 3, 4])
child_obx = obx(parent1, parent2, [1, 3, 4])

print("Padre 1:", parent1)
print("Padre 2:", parent2)
print("Hijo PBX:", child_pbx)
print("Hijo OBX:", child_obx)
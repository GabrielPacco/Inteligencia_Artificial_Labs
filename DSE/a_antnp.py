padres = {("Juan", "Pérez"): [("Pedro", "Pérez"), ("María", "Pérez")], ("Ana", "García"): [("Pedro", "Pérez"), ("María", "Pérez"), ("Luis", "García")], ("Carlos", "García"): [("Luis", "García")]}
madres = {("María", "Pérez"): [("Pedro", "Pérez"), ("Juan", "Pérez")], ("Luisa", "García"): [("Luis", "García")]}

def son_hermanos(persona1, persona2):
    hijos_padre1 = padres.get(persona1, [])
    hijos_padre2 = padres.get(persona2, [])
    hijos_madre1 = madres.get(persona1, [])
    hijos_madre2 = madres.get(persona2, [])
    return (persona1 != persona2) and ((persona1 in hijos_padre2) or (persona1 in hijos_madre2) or (persona2 in hijos_padre1) or (persona2 in hijos_madre1))

def son_primos(persona1, persona2):
    padres_persona1 = padres.get(persona1, [])
    padres_persona2 = padres.get(persona2, [])
    madres_persona1 = madres.get(persona1, [])
    madres_persona2 = madres.get(persona2, [])
    ancestros_en_comun = set(padres_persona1 + madres_persona1) & set(padres_persona2 + madres_persona2)
    return len(ancestros_en_comun) > 0

def es_tio_o_tia_politica(tio_o_tia, sobrino_o_sobrina):
    hermanos = []
    if tio_o_tia in padres:
        hermanos = padres[tio_o_tia]
    elif tio_o_tia in madres:
        hermanos = madres[tio_o_tia]
    for hermano_o_hermana in hermanos:
        if son_hermanos(hermano_o_hermana, sobrino_o_sobrina):
            return True
    return False

def obtener_hermanos(nombre, apellido):
    hermanos = []
    for persona, hijos in padres.items():
        if persona != (nombre, apellido) and (nombre, apellido) in hijos:
            hermanos.append(persona)
    for persona, hijos in madres.items():
        if persona != (nombre, apellido) and (nombre, apellido) in hijos:
            hermanos.append(persona)
    return hermanos

def obtener_primos(nombre, apellido):
    primos = []
    for persona, hijos in padres.items():
        if (nombre, apellido) in hijos:
            for hermano_o_hermana in hijos:
                primos.extend([hijo for hijo in padres.get(hermano_o_hermana, []) if hijo != (nombre, apellido)])
                primos.extend([hijo for hijo in madres.get(hermano_o_hermana, []) if hijo != (nombre, apellido)])
    for persona, hijos in madres.items():
        if (nombre, apellido) in hijos:
            for hermano_o_hermana in hijos:
                primos.extend([hijo for hijo in padres.get(hermano_o_hermana, []) if hijo != (nombre, apellido)])
                primos.extend([hijo for hijo in madres.get(hermano_o_hermana, []) if hijo != (nombre, apellido)])
    return primos

# Ejemplos de uso
print(son_hermanos(("Pedro", "Pérez"), ("María", "Pérez"))) # True
print(son_hermanos(("Juan", "Pérez"), ("Luis", "García"))) # False
print(son_primos(("Pedro", "Pérez"), ("Luis", "García"))) # True
print(son_primos(("Juan", "Pérez"), ("Luisa", "García"))) # False
print(es_tio_o_tia_politica(("Juan", "Pérez"), ("Luis", "García"))) # True
print(es_tio_o_tia_politica(("Ana", "García"), ("Luis", "García"))) # False
print(obtener_hermanos("Pedro", "Pérez")) # [("María", "Pérez")]
print(obtener_primos("Pedro", "Pérez")) # [("Luis", "García")]
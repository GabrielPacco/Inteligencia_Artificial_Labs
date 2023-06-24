padres = {"Juan": ["Pedro", "María"], "Ana": ["Pedro", "María", "Luis"], "Carlos": ["Luis"]}
madres = {"María": ["Pedro", "Juan"], "Luisa": ["Luis"]}

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

# Ejemplos de uso
print(son_hermanos("Pedro", "María")) # True
print(son_hermanos("Juan", "Luis")) # False
print(son_primos("Pedro", "Luis")) # True
print(son_primos("Juan", "Luisa")) # False
print(es_tio_o_tia_politica("Juan", "Luis")) # True
print(es_tio_o_tia_politica("Ana", "Luis")) # False
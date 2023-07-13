class Persona:
    def __init__(self, nombre, genero):
        self.nombre = nombre
        self.genero = genero
        self.padre = None
        self.madre = None

def asignar_padre(padre, hijo):
    hijo.padre = padre

def asignar_madre(madre, hijo):
    hijo.madre = madre

def son_hermanos(persona1, persona2):
    return (
        persona1.padre == persona2.padre and
        persona1.madre == persona2.madre and
        persona1 != persona2
    )

def son_primos(persona1, persona2):
    return (
        persona1.padre != persona2.padre and
        persona1.madre != persona2.madre and
        (persona1.padre == persona2.padre.padre or persona1.madre == persona2.madre.madre)
    )

def es_tio_politico(tio, persona):
    return (
        tio.padre == persona.padre or
        tio.padre == persona.madre or
        tio.madre == persona.padre or
        tio.madre == persona.madre
    )

def es_tia_politica(tia, persona):
    return es_tio_politico(tia, persona)

def obtener_hermanos(nombre):
    persona = arbol_genealogico.get(nombre)
    if persona is None:
        return []
    
    hermanos = []
    for persona_actual in arbol_genealogico.values():
        if son_hermanos(persona_actual, persona):
            hermanos.append(persona_actual.nombre)
    
    return hermanos

def obtener_primos(nombre):
    persona = arbol_genealogico.get(nombre)
    if persona is None:
        return []
    
    primos = []
    for persona_actual in arbol_genealogico.values():
        if son_primos(persona_actual, persona):
            primos.append(persona_actual.nombre)
    
    return primos

def obtener_tios_politicos(nombre):
    persona = arbol_genealogico.get(nombre)
    if persona is None:
        return []
    
    tios_politicos = []
    for persona_actual in arbol_genealogico.values():
        if es_tio_politico(persona_actual, persona):
            tios_politicos.append(persona_actual.nombre)
    
    return tios_politicos

def obtener_tias_politicas(nombre):
    persona = arbol_genealogico.get(nombre)
    if persona is None:
        return []
    
    tias_politicas = []
    for persona_actual in arbol_genealogico.values():
        if es_tia_politica(persona_actual, persona):
            tias_politicas.append(persona_actual.nombre)
    
    return tias_politicas

# Crear árbol genealógico
arbol_genealogico = {}
juan = Persona("Juan", "Hombre")
ana = Persona("Ana", "Mujer")
maria = Persona("Maria", "Mujer")
pedro = Persona("Pedro", "Hombre")
pablo = Persona("Pablo", "Hombre")
jose = Persona("Jose", "Hombre")

asignar_padre(juan, pedro)
asignar_madre(ana, pedro)
asignar_padre(juan, maria)
asignar_madre(ana, maria)
asignar_padre(pedro, pablo)
asignar_madre(maria, pablo)
asignar_padre(pedro, jose)
asignar_madre(maria, jose)

arbol_genealogico[juan.nombre] = juan
arbol_genealogico[ana.nombre] = ana
arbol_genealogico[maria.nombre] = maria
arbol_genealogico[pedro.nombre] = pedro
arbol_genealogico[pablo.nombre] = pablo
arbol_genealogico[jose.nombre] = jose

# Consultas
nombre_persona = "Pedro"
print("Hermanos de", nombre_persona + ":", obtener_hermanos(nombre_persona))
print("Primos de", nombre_persona + ":", obtener_primos(nombre_persona))
print("Tíos políticos de", nombre_persona + ":", obtener_tios_politicos(nombre_persona))
print("Tías políticas de", nombre_persona + ":", obtener_tias_politicas(nombre_persona))

class Persona:
    def __init__(self, nombre, genero):
        self.nombre = nombre
        self.genero = genero
        self.padre = None
        self.madre = None
        self.pareja = None

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
    hermanos_padre = obtener_hermanos(persona.padre.nombre)
    hermanos_madre = obtener_hermanos(persona.madre.nombre)
    hermanos = hermanos_padre + hermanos_madre
    
    for hermano in hermanos:
        if tio.nombre == arbol_genealogico[hermano].pareja:
            return True
    
    return False

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

def obtener_padre(nombre):
    padre = arbol_genealogico.get(nombre).padre
    if padre is None:
        return "No se ha asignado un padre a esta Persona"
    
    return padre.nombre

def obtener_madre(nombre):
    madre = arbol_genealogico.get(nombre).madre
    if madre is None:
        return "No se ha asignado una madre a esta Persona"
    
    return madre.nombre

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
nombre_persona = "Maria"
print("Hermanos de", nombre_persona + ":", obtener_hermanos(nombre_persona))
print("Primos de", nombre_persona + ":", obtener_primos(nombre_persona))
print("Tíos políticos de", nombre_persona + ":", obtener_tios_politicos(nombre_persona))
print("Tías políticas de", nombre_persona + ":", obtener_tias_politicas(nombre_persona))
print("Padre de", nombre_persona + ":", obtener_padre(nombre_persona))
print("Madre de", nombre_persona + ":", obtener_madre(nombre_persona))
class Persona:
    def __init__(self, nombre, genero):
        self.nombre = nombre
        self.genero = genero
        self.padre = None
        self.madre = None

def Papa(X, Y):
    Y.padre = X

def Mama(Z, Y):
    Y.madre = Z

def Hermano(A, B):
    if A.padre == B.padre and A.madre == B.madre and A != B:
        return True
    else:
        return False

def Primo(A, B):
    if A.padre != B.padre and A.madre != B.madre and (A.padre == B.padre.padre or A.madre == B.madre.madre):
        return True
    else:
        return False

def TioPolitico(A, B):
    if A.padre == B.padre or A.padre == B.madre or A.madre == B.padre or A.madre == B.madre:
        return True
    else:
        return False

def TiaPolitica(A, B):
    if A.padre == B.padre or A.padre == B.madre or A.madre == B.padre or A.madre == B.madre:
        return True
    else:
        return False

def obtener_hermanos(nombre):
    hermanos = []
    persona = arbol_genealogico[nombre]
    for persona_actual in arbol_genealogico.values():
        if persona_actual.nombre != nombre and Hermano(persona_actual, persona):
            hermanos.append(persona_actual.nombre)
    return hermanos

def obtener_primos(nombre):
    primos = []
    persona = arbol_genealogico[nombre]
    for persona_actual in arbol_genealogico.values():
        if persona_actual.nombre != nombre and Primo(persona_actual, persona):
            primos.append(persona_actual.nombre)
    return primos

def obtener_tios_politicos(nombre):
    tios_politicos = []
    persona = arbol_genealogico[nombre]
    for persona_actual in arbol_genealogico.values():
        if persona_actual.nombre != nombre and TioPolitico(persona_actual, persona):
            tios_politicos.append(persona_actual.nombre)
    return tios_politicos

def obtener_tias_politicas(nombre):
    tias_politicas = []
    persona = arbol_genealogico[nombre]
    for persona_actual in arbol_genealogico.values():
        if persona_actual.nombre != nombre and TiaPolitica(persona_actual, persona):
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

Papa(juan, pedro)
Mama(ana, pedro)
Papa(juan, maria)
Mama(ana, maria)
Papa(pedro, pablo)
Mama(maria, pablo)
Papa(pedro, jose)
Mama(maria, jose)

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

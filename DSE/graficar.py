import networkx as nx
import matplotlib.pyplot as plt

class ArbGen:
    def __init__(self):
        self.ID = {}
        self.padres = []
    
    def getGen(self, id):
        gen = 1
        while id != 1:
            id = self.padres[id]
            gen += 1
        return gen
    
    def genDif(self, id1, id2):
        diff = self.getGen(id1) - self.getGen(id2)
        return abs(diff)
    
    def LCA(self, id1, id2):
        if id1 == id2:
            return 0
        else:
            g1 = self.getGen(id1)
            g2 = self.getGen(id2)
            while id1 != id2:
                if g1 < g2:
                    id2 = self.padres[id2]
                    g2 -= 1
                elif g1 > g2:
                    id1 = self.padres[id1]
                    g1 -= 1
                else:
                    id1 = self.padres[id1]
                    id2 = self.padres[id2]
                    g1 -= 1
                    g2 -= 1
                if id1 == 1 or id2 == 1:
                    return 1
            return id1
    
    def gen_anc(self, id1, gen):
        if self.getGen(id1) <= gen:
            return id1
        while self.getGen(id1) != gen:
            id1 = self.padres[id1]
        return id1
    
    def genPref(self, gen, grand=False):
        if gen <= 2:
            return ""
        if gen == 3:
            return "Bis"
        ans = ""
        for i in range(3, gen):
            ans += "Tatara"
        return ans
    
    def relacion(self, id1, id2):
        if self.LCA(id1, id2) == 1:
            return "No tienen parentesco"
        if self.padres[id1] == self.padres[id2]:
            return "Hermanos" if id1 != id2 else "Misma persona"
        if id1 == self.LCA(id1, id2):
            diff = self.genDif(id1, id2)
            if diff == 1:
                return "Padre/madre"
            if diff == 2:
                return "Abuelo/abuela"
            pref = self.genPref(self.genDif(id1, id2))
            pref += "abuelo"
            return pref
        if id2 == self.LCA(id1, id2):
            diff = self.genDif(id1, id2)
            if diff == 1:
                return "Hijo/hija"
            if diff == 2:
                return "Nieto/nieta"
            pref = self.genPref(self.genDif(id1, id2))
            pref += "nieto"
            return pref
        if self.padres[self.LCA(id1, id2)] == self.padres[self.LCA(id1, id2)]:
            pref = self.genPref(self.genDif(id1, id2))
            pref += "Tio/tia"
            return pref
        if self.padres[id2] == self.padres[self.gen_anc(id1, self.getGen(id2))]:
            pref = self.genPref(self.genDif(id1, id2))
            pref += "Sobrino/sobrina"
            return pref
        return "Primos"
    
    def build(self, input_data):
        cur_ID = 2
        hs = []
        ps = []
        for hijo, padre in input_data:
            if hijo not in self.ID:
                self.ID[hijo] = cur_ID
                cur_ID += 1
            if padre not in self.ID:
                self.ID[padre] = cur_ID
                cur_ID += 1
            hs.append(hijo)
            ps.append(padre)
        
        self.padres = [1] * (len(self.ID) + 10)
        for i in range(len(hs)):
            self.padres[self.ID[hs[i]]] = self.ID[ps[i]]

        G = nx.DiGraph()
        for hijo, padre in self.ID.items():
            if padre != 1:
                G.add_edge(padre, hijo)
        
        return G

    def plot_tree(self):
        G = self.build(input_data)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_size=1500, node_color="lightblue", font_size=12, edge_color="gray", arrows=False)
        plt.title("Árbol Genealógico")
        plt.show()

arbol = ArbGen()
input_data = [
    ("Juan", "Maria"),
    ("Carlos", "Laura"),
    ("Roberto", "Ana"),
    ("Pedro", "Luis"),
    ("Andres", "Luis"),
    ("Miguel", "Daniel"),
    ("Alejandro", "Sofia"),
    ("David", "Patricia"),
    ("Ricardo", "Carolina"),
    ("Javier", "Andrea"),
    ("Guillermo", "Valentina"),
    ("Hugo", "Isabella"),
    ("Rafael", "Natalia"),
    ("Francisco", "Ana"),
    ("Martin", "Camila"),
    ("Eduardo", "Victoria"),
    ("Luis", "Gabriela"),
    ("Pepe", "Gabriela"),
    ("Renzo", "Pepe"),
    ("Gabriel", "Pepe"),
    ("Sebastian", "Gabriel"),
    ("SebasJr", "Sebastian")
]
arbol.build(input_data)
arbol.plot_tree()

# Tio
print(f"Pepe - Andres: {arbol.relacion(arbol.ID['Pepe'], arbol.ID['Andres'])}")
# Abuelo
print(f"Gabriela - Pedro: {arbol.relacion(arbol.ID['Gabriela'], arbol.ID['Pedro'])}")
# Sobrino
print(f"Pedro - Pepe: {arbol.relacion(arbol.ID['Pedro'], arbol.ID['Pepe'])}")
# Primos
print(f"Pedro - Renzo: {arbol.relacion(arbol.ID['Pedro'], arbol.ID['Renzo'])}")
# Padre/Madre
print(f"Gabriela - Pepe: {arbol.relacion(arbol.ID['Gabriela'], arbol.ID['Pepe'])}")
# Hermanos
print(f"Pepe - Luis: {arbol.relacion(arbol.ID['Pepe'], arbol.ID['Luis'])}")

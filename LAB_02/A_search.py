from queue import PriorityQueue

class Estado:
    def _init_(self, tablero, g, h, movimiento_anterior):
        self.tablero = tablero
        self.g = g # costo acumulado
        self.h = h # estimación heurística
        self.movimiento_anterior = movimiento_anterior

    def f(self):
        return self.g + self.h

    def _lt_(self, otro):
        return self.f() < otro.f()

    def _eq_(self, otro):
        return self.tablero == otro.tablero

def pos_cero(tablero):
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == 0:
                return i, j

def generar_movimientos(tablero):
    movimientos = []
    i, j = pos_cero(tablero)
    if i > 0:
        arriba = [fila[:] for fila in tablero]
        arriba[i][j], arriba[i-1][j] = arriba[i-1][j], arriba[i][j]
        movimientos.append(Estado(arriba, 1, h(arriba), "Abajo"))
    if i < 2:
        abajo = [fila[:] for fila in tablero]
        abajo[i][j], abajo[i+1][j] = abajo[i+1][j], abajo[i][j]
        movimientos.append(Estado(abajo, 1, h(abajo), "Arriba"))
    if j > 0:
        izquierda = [fila[:] for fila in tablero]
        izquierda[i][j], izquierda[i][j-1] = izquierda[i][j-1], izquierda[i][j]
        movimientos.append(Estado(izquierda, 1, h(izquierda), "Derecha"))
    if j < 2:
        derecha = [fila[:] for fila in tablero]
        derecha[i][j], derecha[i][j+1] = derecha[i][j+1], derecha[i][j]
        movimientos.append(Estado(derecha, 1, h(derecha), "Izquierda"))
    return movimientos

def h(tablero):
    # heurística: distancia Manhattan
    distancia = 0
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == 0:
                continue
            x, y = divmod(tablero[i][j]-1, 3)
            distancia += abs(x-i) + abs(y-j)
    return distancia


def a_estrella(inicial, final):
    abierta = PriorityQueue()
    abierta.put(inicial)
    cerrada = set()
    i = 1
    with open("a.txt", "w") as archivo:
        archivo.write("Nombre: a\nBúsqueda: A*\nEstado inicial: " + str(inicial.tablero) + "\nEstado final: " + str(final.tablero) + "\n\n")
        while not abierta.empty():
            actual = abierta.get()
            archivo.write("Iteración " + str(i) + "\n")
            archivo.write("Abierta: ")
            for estado in abierta.queue:
                archivo.write(str(estado.tablero) + " ")
            archivo.write("\nCerrada: ")
            for estado in cerrada:
                archivo.write(str(estado.tablero) + " ")
            archivo.write("\nActual: " + str(actual.tablero) + " (f=" + str(actual.f()) + ", g=" + str(actual.g) + ", h=" + str(actual.h) + ", movimiento=" + str(actual.movimiento_anterior) + ")\n")
            cerrada.add(actual)
            if actual == final:
                archivo.write("\nSolución encontrada:\n")
                camino = []
                while actual.movimiento_anterior:
                    camino.append((actual.movimiento_anterior, actual.tablero))
                    actual = actual.movimiento_anterior
                camino.reverse()
                for movimiento, tablero in camino:
                    archivo.write(movimiento + "\n" + str(tablero) + "\n")
                break
            for movimiento in generar_movimientos(actual.tablero):
                if movimiento in cerrada:
                    continue
                if movimiento not in abierta.queue:
                    abierta.put(movimiento)
                elif movimiento.g < actual.g:
                    abierta.queue.remove(movimiento)
                    abierta.put(movimiento)
            i += 1
            archivo.write("\n")
        archivo.write("Nodos expandidos: " + str(i) + "\n")
        archivo.write("Nodos visitados: " + str(len(cerrada)) + "\n")
        archivo.write("Profundidad de la solución: " + str(len(camino)) + "\n")
        archivo.write("Costo de la solución: " + str(final.g) + "\n")
        archivo.write("Factor de ramificación efectivo: " + str(i**(1/len(cerrada))) + "\n")


if __name__ == "_main_":
    inicial = Estado([[1, 3, 4], [8, 6, 2], [7, 0, 5]], 0, h([[1, 3, 4], [8, 6, 2], [7, 0, 5]]), None)
    final = Estado([[1, 2, 3], [4, 5, 6], [7, 8, 0]], 0, h([[1, 2, 3], [4, 5, 6], [7, 8, 0]]), None)
    a_estrella(inicial, final)
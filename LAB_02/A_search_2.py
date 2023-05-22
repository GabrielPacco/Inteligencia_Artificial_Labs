import heapq

class Node:
    def __init__(self, data, level, fval):
        self.data = data
        self.level = level
        self.fval = fval

    def gen_child(self):
        x, y = self.search(self.data, ' ')
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            hij = self.move(self.data, x, y, i[0], i[1])
            if hij is not None:
                children.append(Node(hij, self.level + 1, 0))
        return children

    def move(self, puz, x1, y1, x2, y2):
        if 0 <= x2 < len(self.data) and 0 <= y2 < len(self.data):
            temp_puz = [row[:] for row in puz]
            temp_puz[x1][y1], temp_puz[x2][y2] = temp_puz[x2][y2], temp_puz[x1][y1]
            return temp_puz
        else:
            return None

    def search(self, puz, x):
        for i in range(len(puz)):
            for j in range(len(puz[i])):
                if puz[i][j] == x:
                    return i, j

    def __lt__(self, other):
        return self.fval < other.fval

class Puzzle:
    def __init__(self, size):
        self.n = size
        self.open = []
        self.closed = []

    def start(self):
        return [[2, 8, 3], [1, 6, 4], [7, ' ', 5]]

    def end(self):
        return [[1, 2, 3], [8, ' ', 4], [7, 6, 5]]

    def f(self, start, goal):
        return self.h(start.data, goal) + start.level

    def h(self, start, goal):
        return sum(start[i][j] != goal[i][j] and start[i][j] != ' ' for i in range(len(start)) for j in range(len(start[i])))

    def show(self, matriz):
        text.write('[' + ', '.join(str(cell) for row in matriz for cell in row) + '];')

    def dat(self, start, goal):
        self.show(start.data)
        text.writelines(["g=", str(start.level), "; h=", str(self.h(start.data, goal)), "; f=",
                          str(self.h(start.data, goal) + start.level), "\n"])

    def process(self):
        text.writelines(["Gabriel Pacco Huaraca \n", "Search A*\n"])
        text.write("Estado start \n")
        start = self.start()
        self.show(start)
        text.write("\n---------------------------------------\n")
        text.write("Estado end \n")
        goal = self.end()
        self.show(goal)
        text.write("\n---------------------------------------\n")
        start = Node(start, 0, 0)
        start.fval = self.f(start, goal)
        hval = self.h(start.data, goal)
        text.write("Open: \n")
        self.show(start.data)
        text.writelines(["g=", str(start.level), "; h=", str(hval), "; f=", str(start.fval), "\nClosed: "])
        text.write("\n--------------------------------------- \n")
        heapq.heappush(self.open, (start.fval, start))
        it = 0
        while self.open:
            cur = heapq.heappop(self.open)[1]
            it += 1
            text.writelines(["Iteracion ", str(it), "\n"])
            text.write("Open: \n")
            for i in cur.gen_child():
                i.fval = self.f(i, goal)
                self.dat(i, goal)
                heapq.heappush(self.open, (i.fval, i))
            text.write("Closed: \n")
            self.dat(cur, goal)
            text.write("\n---------------------------------------\n")
            if self.h(cur.data, goal) == 0:
                break
            self.closed.append(cur)

text = open('resultado.txt', 'w')
puz = Puzzle(3)
puz.process()
text.close()

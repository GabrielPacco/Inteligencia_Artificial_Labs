import networkx as nx
import matplotlib.pyplot as plt
from queue import PriorityQueue
from PIL import Image, ImageDraw, ImageFont

class Puzzle:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal
        self.n = int(len(initial) ** 0.5)

    def h(self, state):
        # heuristic function: number of misplaced tiles
        return sum(s != g for s, g in zip(state, self.goal))

    def astar(self):
        open_list = PriorityQueue()
        open_list.put((0, self.initial))
        came_from = {tuple(self.initial): None}
        cost_so_far = {tuple(self.initial): 0}
        graph = nx.DiGraph()
        graph.add_node(tuple(self.initial))

        while not open_list.empty():
            _, current = open_list.get()
            current_tuple = tuple(current)
            if current == self.goal:
                break

            empty_index = current.index(0)
            x, y = empty_index % self.n, empty_index // self.n

            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.n and 0 <= new_y < self.n:
                    neighbor = current.copy()
                    neighbor_index = new_y * self.n + new_x
                    neighbor[empty_index], neighbor[neighbor_index] = neighbor[neighbor_index], neighbor[empty_index]
                    neighbor_tuple = tuple(neighbor)

                    new_cost = cost_so_far[current_tuple] + 1
                    if neighbor_tuple not in cost_so_far or new_cost < cost_so_far[neighbor_tuple]:
                        cost_so_far[neighbor_tuple] = new_cost
                        priority = new_cost + self.h(neighbor)
                        open_list.put((priority, neighbor))
                        came_from[neighbor_tuple] = current_tuple
                        graph.add_edge(current_tuple, neighbor_tuple)

        return came_from, cost_so_far[current_tuple], graph

    def state_to_image(self, state):
        # create image of state
        size = 50
        img = Image.new('RGB', (self.n * size, self.n * size), color='white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', size=20)

        for i in range(self.n):
            for j in range(self.n):
                x1, y1 = j * size + 2, i * size + 2
                x2, y2 = (j+1) * size - 2, (i+1) * size - 2
                draw.rectangle([x1,y1,x2,y2], outline='black')
                if state[i*self.n+j] != 0:
                    draw.text((x1+size/3,y1+size/3), str(state[i*self.n+j]), fill='black', font=font)

        return img

    def display_solution(self):
        came_from, _, graph = self.astar()

        # reconstruct path
        current = tuple(self.goal)
        path = [current]
        while current != tuple(self.initial):
            current = came_from[current]
            path.append(current)

        # plot tree
        pos = nx.kamada_kawai_layout(graph)
        nx.draw(graph, pos=pos)

        # plot path
        nx.draw_networkx_edges(graph, pos=pos,
                               edgelist=[(path[i], path[i+1]) for i in range(len(path)-1)],
                               edge_color='r', width=2)

        # add labels to nodes
        labels = {}
        for node in graph.nodes():
            img = self.state_to_image(node)
            labels[node] = plt.imshow(img)
            labels[node].set_zorder(10)
            
        nx.draw_networkx_labels(graph,pos=pos,
                                labels=labels,
                                font_size=8,
                                font_color='w')

        plt.show()


initial_state = [2 ,8 ,3 ,1 ,6 ,4 ,7 ,0 ,5]
goal_state = [1 ,2 ,3 ,8 ,0 ,4 ,7 ,6 ,5]
puzzle = Puzzle(initial_state, goal_state)
puzzle.display_solution()

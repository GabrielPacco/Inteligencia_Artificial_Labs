import matplotlib.pyplot as plt
from queue import PriorityQueue

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

        return came_from, cost_so_far[current_tuple]

    def display_solution(self):
        came_from, _ = self.astar()

        # reconstruct path
        current = tuple(self.goal)
        path = [current]
        while current != tuple(self.initial):
            current = came_from[current]
            path.append(current)

        # plot path
        fig, axs = plt.subplots(1, len(path), figsize=(len(path) * 2, 2))

        for i in range(len(path)):
            state = path[len(path) - i - 1]
            data = [[int(c) for c in state[j:j+self.n]] for j in range(0,len(state),self.n)]
            axs[i].pcolor(data, cmap='Greens', edgecolors='k', linewidths=1)

            # add numbers to tiles
            for j in range(len(state)):
                if state[j] != 0:
                    axs[i].text(j % self.n + 0.5, j // self.n + 0.5, int(state[j]), ha='center', va='center', color='black')

            axs[i].axis('off')

        plt.show()


initial_state = [2 ,8 ,3 ,1 ,6 ,4 ,7 ,0 ,5]
goal_state = [1 ,2 ,3 ,8 ,0 ,4 ,7 ,6 ,5]
puzzle = Puzzle(initial_state, goal_state)
puzzle.display_solution()

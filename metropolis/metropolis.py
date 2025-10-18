import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import random

class Graph():
    def __init__(self, size):
        self.adjMatrix = [[0]*size for i in range(size)]
        self.size = size
        self.adjMatrix = np.array(self.adjMatrix)

    def add_edge(self, v1, v2):
        if self.adjMatrix[v1][v2] == 1:
            return
        self.adjMatrix[v1][v2] = 1
        self.adjMatrix[v2][v1] = 1

    def remove_edge(self, v1, v2):
        if self.adjMatrix[v1][v2] == 0:
            return
        self.adjMatrix[v1][v2] = 0
        self.adjMatrix[v2][v1] = 0

    def show_graph(self):
        # print(self.adjMatrix)
        for i in range(self.size):
            for j in range(self.size):
                print(self.adjMatrix[i][j], end=' ')
            print()

    def neighbors(self, v):
        return [i for i in range(self.size) if self.adjMatrix[v][i] == 1]

    # def check_num_conflicts(self, colouring):
    #     for i in range(self.size):
    #         for j in range(self.size):
    #             for u in graph.neighbors(i)

def metropolis(graph, k, num_steps, start_colouring):
    current = start_colouring.copy()
    samples = [current.copy()]
    num_conflicts = []

    for _ in range(num_steps):
        v = np.random.randint(0, graph.size)
        new_colour = np.random.randint(0, k)

        if new_colour != current[v]:
            valid = True
            for u in graph.neighbors(v):
                if current[u] == new_colour:
                    valid = False
                    break
            if valid:
                current[v] = new_colour
        # num_conflicts = check_num_conflicts(current)
        # num_conflicts.append(num_conflicts)
        samples.append(current.copy())
    return samples

g = Graph(5)
for _ in range(random.randint(10, 20)):
    v1, v2 = random.sample(range(5), 2)
    g.add_edge(v1, v2)

k = 25
num_steps = 1500
start_colouring = np.random.randint(0, k, g.size)
print(start_colouring)
samples = metropolis(g, k, num_steps, start_colouring)

G = nx.from_numpy_array(g.adjMatrix)

# pos = nx.spring_layout(G)

# fig, ax = plt.subplots(figsize=(10, 8))
# nx.draw(G, node_color=samples[1353], cmap=plt.cm.Spectral)
# print(samples[1499])
nx.draw(G, node_color=samples[1499], cmap=plt.cm.Spectral)

# # plt.plot(g)
# def update(frame):
#     ax.clear()
#     current = samples[frame]

# anim = animation.FuncAnimation(g, update, frames=1500, interval=50)

plt.show()

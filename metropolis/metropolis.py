import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import random
# import manim

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

# g = graph(3)
# g.add_edge(0,1)
# g.add_edge(1,2)
# g.add_edge(2,0)

# plt.plot(g)
# plt.show()
g = Graph(random.randint(5,10))
for _ in range(random.randint(10, 30)):
    v1, v2 = random.sample(range(g.size), 2)

    g.add_edge(v1, v2)

k = g.size
num_steps = 1500
start_colouring = np.random.randint(0, k, g.size)
print(start_colouring)
samples = metropolis(g, k, num_steps, start_colouring)

G = nx.from_numpy_array(g.adjMatrix)
pos = nx.spring_layout(G, seed=42)

fig, ax = plt.subplots(figsize=(6, 5))

nodes = nx.draw_networkx_nodes(G, pos, node_color=samples[0], cmap=plt.cm.Spectral, ax=ax)
edges = nx.draw_networkx_edges(G, pos, ax=ax)

def update(frame):
    ax.clear()
    ax.set_title(f"Step {frame}")
    nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_color=samples[frame], cmap=plt.cm.Spectral, ax=ax)

anim = animation.FuncAnimation(fig, update, frames=len(samples), interval=100)
# pos = nx.spring_layout(G)

# fig, ax = plt.subplots(figsize=(10, 8))
# # nx.draw(G, node_color=samples[1353], cmap=plt.cm.Spectral)
# print(samples[1499])
# nx.draw(G, node_color=samples[1499], cmap=plt.cm.Spectral)

# # plt.plot(g)
# def update(frame):
#     ax.clear()
#     current = samples[frame]

# anim = animation.FuncAnimation(g, update, frames=1500, interval=50)

plt.show()

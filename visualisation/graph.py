import numpy as np

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
        for i in range(self.size):
            for j in range(self.size):
                print(self.adjMatrix[i][j], end=' ')
            print()

    def neighbors(self, v):
        return [i for i in range(self.size) if self.adjMatrix[v][i] == 1]

    def check_num_conflicts(self, colouring):
        conflicts = 0
        for i in range(self.size):
            for j in self.neighbors(i):
                if i < j and colouring[i] == colouring[j]:
                    conflicts += 1
        return conflicts
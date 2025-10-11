import numpy as np
import matplotlib.pyplot as plt

class Graph():
    def __init__(self, size):
        self.adjMatrix = [[0]*size for i in range(size)]
        self.size = size

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

    def add_colour(self, v1, v2, colour):
        return

    def check_valid_colourings(self, v1, v2):
        return


# General metropolis definition
def metropolis(target_distribution, initial_state, proposal_std, num_samples):
    samples = [initial_state]
    current_state = initial_state

    for _ in range(num_samples - 1):
        proposed_state = current_state + np.random.normal(0, proposal_std)

        acceptance_ratio = target_distribution(proposed_state) / target_distribution(current_state)
        alpha = min(1, acceptance_ratio)

        if np.random.rand() < alpha:
            current_state = proposed_state
        samples.append(current_state)

    return samples


if __name__ == '__main__':
    graph = Graph
    graph.__init__(graph, 5)
    graph.add_edge(graph, 0, 0)
    graph.add_edge(graph, 2, 3)
    graph.add_edge(graph, 3, 2)
    graph.add_edge(graph, 4, 0)

    # graph.remove_edge(graph, 0, 0)
    graph.show_graph(graph)
    
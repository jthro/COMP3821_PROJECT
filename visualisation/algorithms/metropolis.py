import numpy as np

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
        samples.append(current.copy())
    return samples

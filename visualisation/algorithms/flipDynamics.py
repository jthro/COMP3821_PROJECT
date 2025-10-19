import numpy as np
from collections import deque

def flipDynamics(graph, k, num_steps, start_colouring):
    current = start_colouring.copy()
    samples = [current.copy()]

    ## TODO: research what to make this
    Pl = 1

    for _ in range(num_steps):
        v = np.random.randint(0, graph.size)
        b = current[v]

        c = np.random.randint(0, k)
        while c == b:
            c = np.random.randint(0, k)

        cluster = set([v])
        queue = deque([v])

        while queue:
            u = queue.pop()
            u_colour = current[u]
            if u_colour == b:
                target_colour = c 
            else:
                target_colour = b
            for n in graph.neighbors(u):
                if current[n] == target_colour and n not in cluster:
                    cluster.add(n)
                    queue.append(n)

        l = len(cluster)
        if l > 0 and np.random.rand() < Pl / l:
            for u in cluster:
                if current[u] == b:
                    current[u] = c
                else:
                    current[u] = b
        samples.append(current.copy())

    return samples

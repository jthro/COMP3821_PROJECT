#!/usr/bin/env python3

import numpy as np

def distance(colouring1, colouring2):
    d = 0
    for i in range(len(colouring1)):
        if colouring1[i] != colouring2[i]:
            d += 1
    return d

def update(graph, colouring, v, c):
    old = colouring[v]
    if c == old:
        return colouring
    for u in graph.neighbors(v):
        if colouring[u] == c:
            return colouring
    colouring[v] = c
    return colouring

def pathCoupling(graph, k, num_steps, start_colouring, start_colouring2):
    x = start_colouring.copy()
    y = start_colouring2.copy()

    x_samples = [x.copy()]
    y_samples = [y.copy()]
    distances = [distance(x, y)]

    for t in range(num_steps):
        v = np.random.randint(0, graph.size)
        c = np.random.randint(0, k)

        x = update(graph, x, v, c)
        y = update(graph, y, v, c)

        x_samples.append(x.copy())
        y_samples.append(y.copy())
        distances.append(distance(x, y))

    return x_samples, y_samples, distances

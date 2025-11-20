import numpy as np

def pathCoupling(graph, k, num_steps, start_colouring, start_colouring2):
    x = start_colouring.copy()
    y = start_colouring2.copy()

    for _ in range(num_steps):


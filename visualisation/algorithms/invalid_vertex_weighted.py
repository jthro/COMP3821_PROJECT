import numpy as np

def make_invalid_neutral_array(graph, colouring, k):
    # number of neighbours with colour
    # 1 row per vertex
    # 1 column pert coloiur
    counts = np.zeros((graph.size, k), dtype=int)
    for u in range(graph.size):
        for v in graph.neighbors(u):
            counts[u][colouring[v]] += 1
    print(counts)
    return counts

def compute_invalid_neutral_count(graph, colouring, invalid_neutral_array, k):
    # For each colour compute the num vertices that would be invalid or netural if recouloured to c
    conflicts = np.zeros(k, dtype=int)

    for v in range(graph.size):
        for c in range(k):
            t = invalid_neutral_array[v][c]
            # print(t)
            if t > 0:
                # invalid case
                conflicts[c] += 1
            elif c == colouring[v]:
                # neutral case
                conflicts[c] += 1
    return conflicts

def invalid_vertex_weighted(graph, k, num_steps, start_colouring):
    # print('waht')
    current = start_colouring.copy()
    samples = [current.copy()]

    invalid_neutral_array = make_invalid_neutral_array(graph, current, k)

    for _ in range(num_steps):
        invalid_neutral_count = compute_invalid_neutral_count(graph, current, invalid_neutral_array, k)

        v = np.random.randint(0, graph.size)

        old_colour = current[v]

        # Update
        valid = True

        for u in graph.neighbors(v):
            if best_colour == current[u]:
                valid =False
                break

        if valid:
            for u in graph.neighbors(v):
                invalid_neutral_array[u][old_colour] -= 1
                invalid_neutral_array[u][best_colour] += 1

                current[v] = best_colour


        samples.append(current.copy())

    return samples

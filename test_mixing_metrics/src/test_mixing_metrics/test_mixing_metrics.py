import jsonlines
import argparse
import numpy as np
import matplotlib.pyplot as plt

def hash_colouring(colouring):
    return hash(tuple(colouring))

def gen_histogram(graph, colourings):
    # index with hash, contains tuple of order, frequency
    ordered_hist = {}
    n_distinct_colourings = 0
    
    for colouring in colourings:
        key = hash_colouring(colouring)
        if key in ordered_hist:
            ordered_hist[key][1] += 1
        else:
            ordered_hist[key] = [n_distinct_colourings, 1, verify_colouring(graph, colouring)]
            n_distinct_colourings += 1

    # turn it into an array
    result = [0] * n_distinct_colourings
    for _, colouring in ordered_hist.items():
        result[colouring[0]] = [colouring[1], colouring[2]]

    return result

# old jethro was too clever by half (quite literally)
# - "the matrix is diagonally symmetrical i just need to fill in the top diagonal"
# idiot
def fix_adjacency_matrix(adjacency):
    for i,row in enumerate(adjacency):
        for j,cell in enumerate(row):
            adjacency[i][j] |= cell

    return adjacency

# 2521 reference
# returns True if valid colouring
def verify_colouring(graph, colouring):
    stack = [0]
    visited = [False] * len(graph)
    while not len(stack) == 0:        
        curr = stack.pop()
        if visited[curr]:
            continue
        
        visited[curr] = True

        for neighbour, edge in enumerate(graph[curr]):
            if not edge or neighbour == curr:
                continue
            
            if colouring[curr] == colouring[neighbour]:
                return False
            
            stack.append(neighbour)

        return True
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with jsonlines.open(args.filename, mode='r') as reader:
        for i in range(0,10):
            trial = reader.read()
            adjacency = trial['graph']
            adjacency = fix_adjacency_matrix(adjacency)
            
            colourings = trial['colourings:']
            histogram = gen_histogram(adjacency, colourings)
            valid = [10 if h[1] else 0 for h in histogram]

            for i,v in enumerate(valid):
                if not v == 0:
                    print(i)
                    break
        
        # x = np.arange(len(histogram))

        # freq = [h[0] for h in histogram]
        # valid = [10 if h[1] else 0 for h in histogram]

        # for i,v in enumerate(valid):
        #     if not v == 0:
        #         print(i)
        #         break
        
        # fig, ax = plt.subplots()
        # ax.plot(x, freq)
        # ax.plot(x, valid, linestyle="--", color="orange")
        # plt.show()

            
            
    
    

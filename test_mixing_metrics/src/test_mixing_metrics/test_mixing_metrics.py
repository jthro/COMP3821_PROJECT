import jsonlines 
import argparse
import numpy as np
import matplotlib.pyplot as plt
import arviz
# import threading 

# PROCEDURE:
# treat each sample as a histogram of colour frequencies
# compute the gelman-rubin R-statistic for every colour
# take the maximum, if this is "close to 1" then the chain is actually mixed


def gelman_rubin(colourings):
    return arviz.rhat(colourings)

# R = \frac{\frac{L-1}{L}W+\frac{1}{L}B}{W}
# W = \frac{1}{J}\sum_{j=1}^J s_j^2
# # B = \frac{L}{J-1}\sum_{j=1}^J(x_j-x)^2
# def gelman_rubin_r_statistic(colourings):
#     L = 
#     chain_main = 1/L + sum()
#     grand_mean = 
#     between_chain_variance = 
#     within_chain_variance = 

#     # Gelman-Rubin calculations
#     gelman_rubin_numerator_part_1 = ((L - 1)/L) * within_chain_variance
#     gelman_rubin_numerator_part_2 = 1/L * between_chain_variance
#     gelman_rubin_numerator = gelman_rubin_numerator_part_1 + gelman_rubin_numerator_part_2
#     gelman_rubin = gelman_rubin_numerator/within_chain_variance

#     return gelman_rubin

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
    print('ehllo')
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    print(args)

    with jsonlines.open(args.filename, mode='r') as reader:
        for i in range(0,2):
            trial = reader.read()
            adjacency = trial['graph']
            adjacency = fix_adjacency_matrix(adjacency)
            
            colourings = trial['colourings:']
            histogram = gen_histogram(adjacency, colourings)
            
            valid = [10 if h[1] else 0 for h in histogram]
            # print(valid)

            # print(colourings)
            current = []
            rhat_values = []
            counter = 0
            for c in colourings:
                current.append(c)
                np_current = np.array(current)
                # print(np_current)
                arviz_type = arviz.convert_to_dataset(np_current)
                value = arviz.rhat(np_current, method="rank")
                rhat_values.append(value)
                counter += 1

                if counter == 1:
                    continue
                print(value)
                if value < 1:
                    print(counter)
                    break

            # print(rhat_values)

            # rhat_values = arviz.rhat(colourings, method="rank")

            # print(arviz.rhat(colourings, method="rank"))
            # print(colourings)
            # for v in valid:
            #     if (gelman_rubin(colourings) == 1):
            #         print(v)
            #         break


            # for i,v in enumerate(valid):
            #     if not v == 0:
            #         print(i)
            #         break
        
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

# print('hello')    

if __name__ == "__main__":
    main()

        
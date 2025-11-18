import jsonlines 
import argparse
import numpy as np
import matplotlib.pyplot as plt
import arviz as az
import threading 

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

def calc_mixing(chains):
    rhat_list = []

    # print(colourings)
    
    # valid = [10 if h[1] else 0 for h cin histogram]
    # print(valid)

    # print(colourings)
    current = []
    rhat_values = []

    for counter, c in enumerate(chains, start=1):
        np_chain = np.array(c)
        
        np_chain = np_chain[:, np.newaxis]
        current.append(np_chain)

    all_chains = np.stack(current, axis=0)

    # print(all_chasins)

    dataset = az.convert_to_dataset(all_chains)
    # print(dataset)

    rhat = az.rhat(dataset, method="rank")


    rhat_list.append(rhat.to_array().values.flatten())

    # NOTE IK THE BELOW IS V MUCH WRONG FOR NOW
    cur = rhat_list[0]
    # print(cur)
    min_value = min(cur)
    # 
    min_index = np.argmin(cur)
    # ]
    print(min_value)
    print(min_index)
    print(rhat_list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    

    with jsonlines.open(args.filename, mode='r') as reader:
        threads = []

        for i in range(0,99):
            chains = []
            for j in range(0, 10):
                trial = reader.read()
                adjacency = trial['graph']
                adjacency = fix_adjacency_matrix(adjacency)
                
                colourings = trial['colourings:']
                histogram = gen_histogram(adjacency, colourings)

                chains.append(colourings)
            t = threading.Thread(target=calc_mixing, args=(chains,))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()
            
            
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

        
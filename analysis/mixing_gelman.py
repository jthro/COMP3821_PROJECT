# PROCEDURE:
# treat each sample as a histogram of colour frequencies
# compute the gelman-rubin R-statistic for every colour
# take the maximum, if this is "close to 1" then the chain is actually mixed
import arviz

## From test_mixing_metrics.py
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
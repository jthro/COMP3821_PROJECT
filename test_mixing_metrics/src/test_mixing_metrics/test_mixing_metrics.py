import jsonlines 
import argparse
import numpy as np
import matplotlib.pyplot as plt
<<<<<<< HEAD
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
=======
import threading
from queue import Queue

>>>>>>> a297e03 (Current status)

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
            ordered_hist[key] = [
                n_distinct_colourings,
                1,
                verify_colouring(graph, colouring),
            ]
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
    for i, row in enumerate(adjacency):
        for j, cell in enumerate(row):
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

def mixing_time(trial):
    adjacency = fix_adjacency_matrix(trial["graph"])

    for i, colouring in enumerate(trial["colourings:"]):
        if verify_colouring(adjacency, colouring):
            return i
    return i


# process a singular jsonl object
def process_obj(obj):
    chain = obj["chain"]
    k = obj["k"]
    nv = obj["nv"]

    return {"chain": chain, "k": k, "nv": nv, "time": mixing_time(obj)}


# process a list of jsonl objects
# intended as a task for one worker thread
def triage_task(task_queue, result_queue):
    while True:
        obj = task_queue.get()
        if obj is None:
            break
        result_queue.put(process_obj(obj))
        task_queue.task_done()


# combine a queue of mixing time results into a table
# intended to recombine the worker thread results
def triage_combine(triage_result_queue):
    return_table = {}
    while not triage_result_queue.empty():
        result = triage_result_queue.get()
        chain = result['chain']
        k = result['k']
        nv = result['nv']
        time = result['time']
        print(chain)
        
        return_table.setdefault(chain, {}).setdefault(k, {}).setdefault(nv, []).append(time)
    print(return_table)
    return return_table


# MAIN
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    task_queue = Queue(maxsize=1028)
    
    threads = []
    result_queue = Queue()
    for _ in range(16):
        t = threading.Thread(target=triage_task, args=(task_queue, result_queue))
        t.start()
        threads.append(t)

    with jsonlines.open(args.filename, mode="r") as reader:
        for i, obj in enumerate(reader):
            task_queue.put(obj)

    for t in range(16):
        task_queue.put(None)
    for t in threads:
        t.join()

    result_table = triage_combine(result_queue)

    print(result_table)
    # mean, standard deviation for each one
    stats = {}
    for chain, ks in result_table.items():
        stats[chain] = {}
        for k, nv_dict in ks.items():
            nvs = sorted(nv_dict.keys())
            means = [np.mean(nv_dict[nv]) for nv in nvs]
            iqrs = [
                np.percentile(nv_dict[nv], 75) - np.percentile(nv_dict[nv], 25)
                for nv in nvs
            ]
            stats[chain][k] = (nvs, means, iqrs)

    colors = {"middleton-bulseco": "blue", "naive-metropolis": "orange"}

    # Get all unique k values across both chains
    all_ks = sorted(
        set(
            list(stats["middleton-bulseco"].keys())
            + list(stats["naive-metropolis"].keys())
        ),
        key=int,
    )

    # Create subplots: one per k
    fig, axes = plt.subplots(len(all_ks), 1, figsize=(8, 5 * len(all_ks)), sharex=True)

    if len(all_ks) == 1:
        axes = [axes]  # Ensure axes is always iterable

    for ax, k in zip(axes, all_ks):
        for chain in ["middleton-bulseco", "naive-metropolis"]:
            if k in stats[chain]:
                nvs, means, iqrs = stats[chain][k]
                ax.errorbar(
                    nvs,
                    means,
                    yerr=iqrs,
                    label=(
                        "Naive Metropolis"
                        if (chain == "naive-metropolis")
                        else "Middleton-Bulseco"
                    ),
                    color=colors[chain],
                    marker="o",
                    capsize=4,
                )
        ax.set_title(f"Mean Mixing Time & IQR for k={k}")
        ax.set_ylabel("Mixing Time")
        ax.legend()

    axes[-1].set_xlabel("nv")
    plt.tight_layout()
    plt.show()


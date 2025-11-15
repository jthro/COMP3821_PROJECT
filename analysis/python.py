import json
import numpy as np
import matplotlib.pyplot as plt

def mdm_mixing_time_np(colourings, block_size, threshold):
    # Convert to NumPy array
    colourings = np.array(colourings)
    num_steps = colourings.shape[0]  
    
    # Need unique coloueing states
    unique_states, encoded = np.unique(colourings, axis=0, return_inverse=True)
    num_states = len(unique_states)
    
    # Divide into blocks, how do we work out block size???
    num_blocks = num_steps // block_size
    blocks = encoded[:num_blocks * block_size].reshape(num_blocks, block_size)
    
    # Frequency array for each blcok and each state
    freqs = np.zeros((num_blocks, num_states), dtype=float)
    for i in range(num_states):
        freqs[:, i] = np.sum(blocks == i, axis=1) / block_size
    
    # Difference between max and min 
    mdm_values = freqs.max(axis=1) - freqs.min(axis=1)
    
    # Drop below some threshold (need to calcaulte)
    mask = mdm_values <= threshold
    if np.any(mask):
        first_block = np.argmax(mask)
        return (first_block + 1) * block_size

    # Doesnt mix
    return num_steps

def process_jsonl(file_path, block_size, threshold):
    data_by_d = {}
    all_mixing_times = []
    i = 0
    print('hi')
    with open(file_path, "r") as f:
        for line in f:
            data = json.loads(line)
            colourings = data["colourings:"]
            nv = data.get("nv")
            k = data.get("k")
            d = data.get("d")

            mix_time = mdm_mixing_time_np(colourings, block_size, threshold)
            all_mixing_times.append(mix_time) 
            if d not in data_by_d:
                data_by_d[d] = []
            data_by_d[d].append(mix_time)
            i += 1
            # print(i, mix_time)

    d_list, avg_mix_times = [], []
    for d, times in sorted(data_by_d.items()):
        d_list.append(d)
        avg_mix_times.append(np.mean(times))
    
    return d_list, avg_mix_times, all_mixing_times  

def plot_mdm(nv_list, avg_mix_times):
    plt.figure(figsize=(10,6))
    plt.plot(nv_list, avg_mix_times, marker='o', linestyle='-', color='blue', label='Average Mixing Time')

    nv_array = np.array(nv_list)
    n_log_n = nv_array * np.log(nv_array)
    n_log_n = n_log_n / np.max(n_log_n) * np.max(avg_mix_times)

    plt.plot(nv_list, n_log_n, linestyle=':', color='red', label=r'$n \log n$')

    plt.xlabel('Maximum degree')
    plt.ylabel('Average Mixing Time')
    plt.title('Mixing Time vs Number of Vertices')
    plt.grid(True, which='both', ls='--', alpha=0.5)
    plt.legend()
    plt.show()


file_path = "output.jsonl"  
# TODO: actually do proper calcs for the numbers here
block_size = 20
threshold = 0.01
print('i')

d_list, avg_mix_times, all_mixing_times = process_jsonl(file_path, block_size, threshold)

plot_mdm(d_list, avg_mix_times)


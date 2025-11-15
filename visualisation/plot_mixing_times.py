#!/usr/bin/env python3

import json
import argparse
import numpy as np
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    n_values, k_values, mixing_times = [], [], []

    with open(args.file) as f:
        for line in f:
            data = json.loads(line)
            colourings = data["colourings:"]
            n = data["nv"]
            d = data["d"]

            # fix delta to n/2
            k_num_colours = d * (n / 2)
            mixing_time = compute_mixing_time(colourings, n)
            n_values.append(n)
            k_values.append(k_num_colours)
            mixing_times.append(mixing_time)

    plt.figure(figsize=(9, 6))
    sc = plt.scatter(n_values, mixing_times, c=k_values)
    plt.colorbar(sc, label="Number of colours (k)")
    plt.xlabel("Number of vertices (n)")
    plt.ylabel("Mixing time (steps)")
    plt.title("Mixing time vs Graph Size")
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.show()

def compute_mixing_time(colourings, n):
    # Arbitrarily chosen nlogn factor and threshold
    k_factor = 0.5
    std_threshold = 0.02
    colourings = np.array(colourings)
    num_samples = len(colourings)
    stds = []

    for t in range(num_samples):
        tail = colourings[t:]
        std = np.std(tail)
        stds.append(std)

        # Return num of steps when within arbitrary threshold
        if std < std_threshold and t >= int(k_factor * n * np.log(n)):
            return t

    # If it doesn't stabilize
    return num_samples

if __name__ == "__main__":
    main()


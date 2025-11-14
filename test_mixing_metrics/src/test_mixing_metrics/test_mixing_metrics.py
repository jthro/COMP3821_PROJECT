import jsonlines
import argparse
import numpy as np
import matplotlib.pyplot as plt

def hash_colouring(colouring):
    return hash(tuple(colouring))

def gen_histogram(colourings):
    # index with hash, contains tuple of order, frequency
    ordered_hist = {}
    n_distinct_colourings = 0
    
    for colouring in colourings:
        key = hash_colouring(colouring)
        if key in ordered_hist:
            ordered_hist[key][1] += 1
        else:
            ordered_hist[key] = [n_distinct_colourings, 1]
            n_distinct_colourings += 1

    # turn it into an array
    result = [0] * n_distinct_colourings
    for _, colouring in ordered_hist.items():
        result[colouring[0]] = colouring[1]

    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with jsonlines.open(args.filename, mode='r') as reader:
        for i in range(0,40):
            reader.read()
            
        colourings = reader.read()['colourings:']
        histogram = gen_histogram(colourings)

        x = np.arange(len(histogram))
        plt.style.use('_mpl-gallery')
        fig, ax = plt.subplots()
        ax.bar(x, histogram, width=1, edgecolor="white", linewidth=0.7)
        plt.show()
        
            
            
    
    

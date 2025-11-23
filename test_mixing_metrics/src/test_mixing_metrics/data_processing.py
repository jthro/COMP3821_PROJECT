import numpy as np

from typing import Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import Counter, defaultdict

from .types import DataEntry, Colouring
from .graph import fix_adjacency_matrix, first_valid_colouring


def parse_obj(obj) -> DataEntry:
    """
    Parse object into DataEntry for a run
    """
    return {
        "chain_name": obj["chain"],
        "colourings": obj["colourings:"],
        "k": obj["k"],
        "shape": obj["shape"],
        "nv": obj["nv"],
        "graph": fix_adjacency_matrix(obj["graph"]),
    }


def process_entry_first_valid_colouring(trial: DataEntry):
    return {
        "chain_name": trial["chain_name"],
        "shape": trial["shape"],
        "nv": trial["nv"],
        "mixing_time": first_valid_colouring(trial["graph"], trial["colourings"]),
    }


def process_obj_first_valid_colouring(obj):
    return process_entry_first_valid_colouring(parse_obj(obj))


def process_file_earliest_mixing_time(f):
    objects = list(f)
    results = []
    with ProcessPoolExecutor(max_workers=16) as executor:
        futures = [
            executor.submit(process_obj_first_valid_colouring, obj) for obj in objects
        ]

        for future in as_completed(futures):
            results.append(future.result())

    return results



def colourings_to_histograms(colourings, k):
    return np.array([np.bincount(c, minlength=k) for c in colourings])
                    

def process_entry_within_mean_covariance(trial: DataEntry):
    histograms = colourings_to_histograms(trial["colourings"], trial["k"])
    
    return {
        "chain_name": trial["chain_name"],
        "k": trial["k"],
        "nv": trial["nv"],
        "n_samples": len(trial["colourings"]),
        "within_mean": histograms.mean(axis=0),
        "within_cov": np.cov(histograms, rowvar=False, bias=False)
    }


def process_obj_within_mean_covariance(obj):
    return process_entry_within_mean_covariance(parse_obj(obj))

    
def process_file_mvprsf(f):
    objects = list(f)
    stats_by_experiment = defaultdict(list)
    
    with ProcessPoolExecutor(max_workers=16) as executor:
        futures = [
            executor.submit(process_obj_within_mean_covariance, obj) for obj in objects
        ]

        for future in as_completed(futures):
            res = future.result()
            key = (res["nv"], res["k"], res["chain_name"])
            stats_by_experiment[key].append(res)

    entries = []

    for key, chains in stats_by_experiment.items():
        m = len(chains)
        k = key[1]
        n_samples = np.array([res["n_samples"] for res in chains])
        n = n_samples[0]

        chain_means = np.vstack([res["within_mean"] for res in chains])
        overall_mean = chain_means.mean(axis=0)

        B = n / (m - 1) * ((chain_means - overall_mean).T @ (chain_means - overall_mean))
        W = np.mean([res["within_cov"] for res in chains], axis=0)
        V_hat = (n-1)/n * W + B / n

        eigenvals = np.linalg.eigvals(np.linalg.pinv(W) @ V_hat)
        R_hat = max(np.real(eigenvals))

        entries.append({
            "chain_name": key[2],
            "k": k,
            "nv": key[0],
            "r_hat": R_hat
        })

    return entries

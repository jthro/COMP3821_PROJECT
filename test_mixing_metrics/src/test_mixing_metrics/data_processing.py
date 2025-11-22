from typing import Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed

from .types import DataEntry
from .graph import fix_adjacency_matrix, first_valid_colouring


def parse_obj(obj) -> DataEntry:
    """
    Parse object into DataEntry for a run
    """
    return {
        "chain_name": obj["chain"],
        "colourings": obj["colourings:"],
        "k": obj["k"],
        "nv": obj["nv"],
        "graph": fix_adjacency_matrix(obj["graph"]),
    }


def process_entry_first_valid_colouring(trial: DataEntry):
    return {
        "chain_name": trial["chain_name"],
        "k": trial["k"],
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

from typing import List, TypedDict
from concurrent.futures import ProcessPoolExecutor, as_completed

AdjacencyMatrix = List[List[bool]]
ExternalAdjacencyMatrix = List[List[int]]

Colouring = List[int]

class DataEntry(TypedDict):
    chain_name: str
    colourings: List[Colouring]
    shape: str
    nv: int
    graph: AdjacencyMatrix
    

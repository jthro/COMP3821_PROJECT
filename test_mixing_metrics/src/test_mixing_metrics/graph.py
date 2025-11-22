# graph.py
# util functions for graphs

from typing import List

from .types import (
    AdjacencyMatrix,
    ExternalAdjacencyMatrix,
    Colouring,
)

from collections import deque


def adjacency_matrix_external_to_internal(
    matrix: ExternalAdjacencyMatrix,
) -> AdjacencyMatrix:
    return [[bool(cell) for cell in row] for row in matrix]


def symmetrise_adjacency_matrix(matrix: AdjacencyMatrix) -> AdjacencyMatrix:
    """
    Symmetrise upper triangular matrix
    """
    return [
        [(matrix[i][j] or matrix[j][i]) if i != j else True for j in range(len(matrix))]
        for i in range(len(matrix))
    ]


def fix_adjacency_matrix(matrix: ExternalAdjacencyMatrix) -> AdjacencyMatrix:
    """
    Converte external representation to internal
    """
    return symmetrise_adjacency_matrix(adjacency_matrix_external_to_internal(matrix))


def valid_colouring_p(graph: AdjacencyMatrix, colouring: Colouring) -> bool:
    """
    Return whether a given colouring is valid
    """
    stack = deque([0])
    visited = [False] * len(colouring)
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
    # end while
    return True


def first_valid_colouring(matrix: AdjacencyMatrix, colourings: List[Colouring]) -> int:
    """
    Return -1 if never valid
    """
    for i, colouring in enumerate(colourings):
        if valid_colouring_p(matrix, colouring):
            return i
    return -1

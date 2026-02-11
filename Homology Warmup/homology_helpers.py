import numpy as np
import galois
from itertools import combinations

def find_p_simplices(K: list[list[int]], p: int) -> list[list[int]]:
    """
    Finds all unique p-simplicies from a simplicial complex K
    
    :param K: The simplicial complex represented as a list of simplicies
    :param p: The dimension of the simplicies to find
    """
    p_simplicies = set()

    for simplex in K:
        faces = sorted(simplex)

        if len(faces) == p+1:
            p_simplicies.add(tuple(faces))
        elif len(faces) > p+1:
            for face in combinations(faces, p+1):
                p_simplicies.add(face)
    
    return [list(simplex) for simplex in p_simplicies]

def find_p_boundary(K: list[list[int]], p: int) -> galois.FieldArray:
    """
    Creates the p-th boundary matrix over GF(2) for the simplicial complex K
    
    :param K: The simplicial complex represented as a list of simplicies
    :param p: The dimension of the boundary operator to compute
    """
    p_simplices = find_p_simplices(K, p)
    prev_simplices = find_p_simplices(K, p-1)
    
    face_to_index = {tuple(sorted(f)): i for i, f in enumerate(prev_simplices)}
    
    GF2 = galois.GF(2)
    matrix = GF2.Zeros((len(prev_simplices), len(p_simplices)))
    
    for j, simplex in enumerate(p_simplices):
        for i in range(len(simplex)):
            face = tuple(sorted(list(simplex)[:i] + list(simplex)[i+1:]))
            if face in face_to_index:
                row_idx = face_to_index[face]
                matrix[row_idx, j] = 1
                
    return matrix

def find_p_betti_number(K: list[list[int]], p: int) -> int:
    """
    Calculates the p-th Betti number (rank of the p-th homology group) of the simplicial complex K.
    
    :param K: The simplicial complex represented as a list of simplicies
    :param p: The dimension of the Betti number to compute
    """
    return find_p_boundary(K, p).null_space().shape[0] - np.linalg.matrix_rank(find_p_boundary(K, p+1))
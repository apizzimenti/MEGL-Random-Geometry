import networkx as nx
import random

def lattice_setup(N):
    G = nx.grid_2d_graph(N, N, periodic=True)
    return G

def is_cycle_winding_vertical(cycle, N):
    for consecutive_edges in zip(cycle, cycle[1:] + [cycle[0]]):
        if abs(consecutive_edges[0][0] - consecutive_edges[1][0]) == N-1:
            return True
    return False

def is_cycle_winding_horizontal(cycle, N):
    for consecutive_edges in zip(cycle, cycle[1:] + [cycle[0]]):
        if abs(consecutive_edges[0][1] - consecutive_edges[1][1]) == N-1:
            return True
    return False

def simulate_percolation(N, p):
    prop_first = -1
    prop_second = -1
    ref_graph = lattice_setup(N)
    sim_graph = lattice_setup(N)
    sim_graph.clear_edges()

    while prop_second == -1:
        random_edge = random.choice(list(ref_graph.edges))
        if random.random() <= p:
            sim_graph.add_edge(*random_edge)
        
        has_vertical_periodic_path = False
        has_horizontal_periodic_path = False

        for cycle in nx.cycle_basis(sim_graph):
            if is_cycle_winding_vertical(cycle, N):
                has_vertical_periodic_path = True
            if is_cycle_winding_horizontal(cycle, N):
                has_horizontal_periodic_path = True
        
        if (has_vertical_periodic_path or has_horizontal_periodic_path) and prop_first == -1:
            prop_first = len(sim_graph.edges) / (2*(N**2))
        if has_vertical_periodic_path and has_horizontal_periodic_path:
            prop_second = len(sim_graph.edges) / (2*(N**2))
    
    return prop_first, prop_second
        

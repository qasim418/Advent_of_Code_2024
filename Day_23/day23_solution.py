from collections import defaultdict

def read_input(file_name):
    """Reads input from the specified file."""
    with open(file_name, 'r') as file:
        connections = [line.strip().split('-') for line in file]
    return connections

def build_graph(connections):
    """Builds an adjacency list graph from connections."""
    graph = defaultdict(set)
    for a, b in connections:
        graph[a].add(b)
        graph[b].add(a)
    return graph

def find_triads(graph):
    """Finds all triads (sets of three interconnected nodes) in the graph."""
    triads = set()
    for node in graph:
        neighbors = graph[node]
        for neighbor1 in neighbors:
            for neighbor2 in neighbors:
                if neighbor1 != neighbor2 and neighbor2 in graph[neighbor1]:
                    triad = tuple(sorted([node, neighbor1, neighbor2]))
                    triads.add(triad)
    return triads

def bron_kerbosch(graph, r, p, x, cliques):
    """Bron-Kerbosch algorithm to find maximal cliques."""
    if not p and not x:
        cliques.append(r)
        return
    for v in list(p):
        bron_kerbosch(
            graph, 
            r.union({v}), 
            p.intersection(graph[v]), 
            x.intersection(graph[v]), 
            cliques
        )
        p.remove(v)
        x.add(v)

def find_maximal_cliques(graph):
    """Finds all maximal cliques in the graph."""
    cliques = []
    bron_kerbosch(graph, set(), set(graph.keys()), set(), cliques)
    return cliques

def find_largest_clique(cliques):
    """Finds the largest clique among all cliques."""
    return max(cliques, key=len)

def generate_password(clique):
    """Generates the password from the largest clique."""
    return ",".join(sorted(clique))

def main():
    # Input file name
    input_file = "Day_23/day23_input.txt"

    # Read input connections
    connections = read_input(input_file)

    # Build the adjacency list graph
    graph = build_graph(connections)

    # Task 1: Find triads
    triads = find_triads(graph)

    # Filter triads containing a node starting with 't'
    triads_with_t = [triad for triad in triads if any(node.startswith('t') for node in triad)]
    print(f"Number of triads containing a node starting with 't': {len(triads_with_t)}")

    # Task 2: Find the largest clique and generate a password
    cliques = find_maximal_cliques(graph)
    largest_clique = find_largest_clique(cliques)
    password = generate_password(largest_clique)
    print(f"Password to the LAN party: {password}")

if __name__ == "__main__":
    main()

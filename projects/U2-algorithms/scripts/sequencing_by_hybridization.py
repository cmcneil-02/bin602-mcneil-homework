"""
Sequencing by Hybridization (SBH) using Eulerian Path
Based on Ch. 8.8 of "An Introduction to Bioinformatics Algorithms"

This scripts solves the SBH problem by constructing a de Bruijn graph
from l-mers and finding an Eulerian path that visits all edges.

Usage: python3 sequencing_by_hybridization.py input.txt

Author: Collin McNeil
Course: BIN602 - Data Mining for Bioinformatics
Date: 12-30-2024
"""

import sys
from collections import defaultdict, deque


def build_debruijn_graph(l_mers):
    """
    Build a de Bruijn graph from l-mers.
    
    In this graph:
    - Vertices are (l-1)-mers
    - Edges represent l-mers (from prefix to suffix)

    Parameters:
        l_mers (list): List of l-mers strings

    Returns:
        dict: Adjacency list representation where keys are (l-1)-mer vertices
                and values are lists of outgoing vertices
    """
    graph = defaultdict(list)

    for l_mer in l_mers:
        # Get the prefix (first l-1 nucleotides)
        prefix = l_mer[:-1]
        # Get the suffix (last l-1 nucleotides)
        suffix = l_mer[1:]
        # Add directed edge from prefix to suffix
        graph[prefix].append(suffix)

    return graph


def get_vertex_degrees(graph):
    """
    Calculate in-degree and out-degree for eac vertex.
    
    Parameters:
        graph (dict): Adjacency list representation of graph
        
    Returns:
        tuple: (in_degrees dict, out_degrees dict)
    """
    in_degrees = defaultdict(int)
    out_degrees = defaultdict(int)

    for vertex in graph:
        out_degrees[vertex] = len(graph[vertex])
        for neighbor in graph[vertex]:
            in_degrees[neighbor] += 1

    return in_degrees, out_degrees


def find_start_vertex(graph, in_degrees, out_degrees):
    """
    Find the starting vertex for Eulerian path.
    
    For an Eulerian path (not cycle):
    - Start vertex has out_degree - in_degree = 1
    - End vertex has in_degree - out_degree = 1
    - All other vertices are balanced

    Parameters:
        graph (dict): Adjacency list
        in_degrees (dict): In-degrees of vertices
        out_degrees (dict): Out-degrees of vertices

    Returns:
        str: Starting vertex for Eulerian path
    """
    # Get all vertices (including those that only appear as destinations)
    all_vertices = set(graph.keys())
    for vertex in graph:
        all_vertices.update(graph[vertex])

    start = None

    # Look for a vertex with out_degree - in_degree = 1 (start of path)
    for vertex in all_vertices:
        out_deg = out_degrees[vertex]
        in_deg = in_degrees[vertex]

        if out_deg - in_deg == 1:
            start = vertex
            break

    # If no such vertex exists, thr graph has an Eulerian cycle
    # Start from any vertex with outgoing edges
    if start is None:
        start = next(iter(graph.keys()))

    return start


def find_eulerian_path(graph):
    """
    Find an Eulerian path in the graph using Hierholzer's algorithm.

    Parameters:
        graph (dict): Adjacency list representation

    Returns:
        list: List of vertices in Eulerian path order
    """
    # Make a copy of the graph to modify it
    graph_copy = defaultdict(list)
    for vertex in graph:
        graph_copy[vertex] = list(graph[vertex])

    # Calculate degrees
    in_degrees, out_degrees = get_vertex_degrees(graph)

    # Find starting vertex
    start = find_start_vertex(graph, in_degrees, out_degrees)

    # Hierholzer's algorithm
    stack = [start]
    path = []

    while stack:
        vertex = stack[-1]

        if graph_copy[vertex]:
            # If there are unvisited edges, follow one
            next_vertex = graph_copy[vertex].pop(0)
            stack.append(next_vertex)
        else:
            # No more edges from this vertex, add to path
            path.append(stack.pop())

    # Path is built in reverse order
    path.reverse()

    return path


def reconstruct_sequence(path):
    """
    Reconstruct the DNA sequence from an Eulerian path.

    The path visits edges (l-mers), so we reconstruct by:
    - Starting with the first vertex (l-1 nucleotides)
    - Adding the last nucleotide from each subsequent vertex

    Parameters:
        path (list): List of vertices in Eulerian path

    Returns:
        str: Reconstructed DNA sequence
    """
    if not path:
        return ""
    
    # Start with the first vertex
    sequence = path[0]

    # Add the last character of each subsequent vertex
    for i in range(1, len(path)):
        sequence += path[i][-1]

    return sequence


def solve_sbh(l_mers):
    """
    Solve the SBH problem.

    Parameters:
        l_mers (list): List of l-mers strings from spectrum

    Returns:
        str: Reconstructed DNA sequence (shortest superstring)
    """
    # Build de Bruijn graph
    graph = build_debruijn_graph(l_mers)

    # Find Eulerian path
    path = find_eulerian_path(graph)

    # Reconstruct sequence from path
    sequence = reconstruct_sequence(path)

    return sequence


def main():
    """
    Main function to handle file I/O and solve SBH problem.
    """
    if len(sys.argv) < 2:
        print("Usage: python3 sequencing_by_hybridization.py input.txt", file=sys.stderr)
        print("  input.txt - file containing one l-mer per line", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]

    # Read l-mers from file
    try:
        with open(input_file, 'r') as f:
            l_mers = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
                print(f"Error: File '{input_file}' not found.", file=sys.stderr)
                sys.exit(1)
    except Exception as e:
                print(f"Error reading file: {e}", file=sys.stderr)
                sys.exit(1)
    
    if not l_mers:
        print("Error: Input file is empty.", file=sys.stderr)
        sys.exit(1)

    # Automatically detect l
    l = len(l_mers[0])
    print(f"Detected l-mer length: {l}")
    print(f"Number of l-mers: {len(l_mers)}")
    print(f"L-mers: {l_mers}")
    print()

    # Solve SBH problem
    result = solve_sbh(l_mers)

    # Output result
    print(f"Reconstructed sequence: {result}")
    print(f"Length: {len(result)}")

if __name__ == "__main__":
    main()
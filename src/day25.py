# Karger's algorithm to find Minimum Cut in an
# undirected, unweighted and connected graph.
import os
import random


# a class to represent an unweighted edge in graph
class Edge:
    def __init__(self, s, d):
        self.src = s
        self.dest = d


# a class to represent a connected, undirected
# and unweighted graph as a collection of edges.
class Graph:

    # V-> Number of vertices, E-> Number of edges
    def __init__(self, v, e):
        self.V = v
        self.E = e

        # graph is represented as an array of edges.
        # Since the graph is undirected, the edge
        # from src to dest is also edge from dest
        # to src. Both are counted as 1 edge here.
        self.edges = []
        self.vertices = []


# A class to represent a subset for union-find
class Subset:
    def __init__(self, p, r):
        self.parent = p
        self.rank = r


# A very basic implementation of Karger's randomized
# algorithm for finding the minimum cut. Please note
# that Karger's algorithm is a Monte Carlo Randomized algo
# and the cut returned by the algorithm may not be
# minimum always
def karger_min_cut(graph):
    # Get data of given graph
    graph_vertex_count = graph.V
    graph_edge_count = graph.E
    edges = graph.edges

    # Allocate memory for creating V subsets.
    subsets = []

    # Create V subsets with single elements
    for vertex_index in range(graph_vertex_count):
        subsets.append(Subset(vertex_index, 0))

    # Initially there are V vertices in contracted graph
    vertex_count = graph_vertex_count

    # Keep contracting vertices until there are 2 vertices.
    while vertex_count > 2:
        # Pick a random edge
        i = random.randrange(graph_edge_count)

        # Find vertices (or sets) of two corners of current edge
        subset1 = find(subsets, edges[i].src)
        subset2 = find(subsets, edges[i].dest)

        # If two corners belong to same subset,
        # then no point considering this edge
        if subset1 == subset2:
            continue

        # Else contract the edge (or combine the corners of edge into one vertex)
        else:
            # print("Contracting edge " + vertices[edges[i].src] + "-" + vertices[edges[i].dest])
            vertex_count -= 1
            union(subsets, subset1, subset2)

    # Now we have two vertices (or subsets) left in
    # the contracted graph, so count the edges between
    # two components and return the count.
    cut_edges = 0
    for i in range(graph_edge_count):
        subset1 = find(subsets, edges[i].src)
        subset2 = find(subsets, edges[i].dest)
        if subset1 != subset2:
            # print(f'Cut edge: {vertices[edges[i].src]} - {vertices[edges[i].dest]}')
            cut_edges += 1

    set_counts = {}
    for subset in subsets:
        parent = subset.parent
        if parent not in set_counts.keys():
            set_counts[parent] = 1
        else:
            set_counts[parent] += 1

    return cut_edges, [*set_counts.values()]


# A utility function to find set of an element vertex (uses path compression technique)
def find(subsets, vertex):
    # find root and make root as parent of vertex (path compression)
    if subsets[vertex].parent != vertex:
        subsets[vertex].parent = find(subsets, subsets[vertex].parent)

    return subsets[vertex].parent


# A function that does union of two sets of x and y (uses union by rank)
def union(subsets, x, y):
    x_root = find(subsets, x)
    y_root = find(subsets, y)

    # Attach smaller rank tree under root of high rank tree (Union by Rank)
    if subsets[x_root].rank < subsets[y_root].rank:
        subsets[x_root].parent = y_root
    elif subsets[x_root].rank > subsets[y_root].rank:
        subsets[y_root].parent = x_root

    # If ranks are same, then make one as root and increment its rank by one
    else:
        subsets[y_root].parent = x_root
        subsets[x_root].rank += 1


# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day25.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


def day_25():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    vertex_set = set()
    edges = []

    for line in lines:
        pieces = line.split(': ')
        name = pieces[0]
        vertex_set.add(name)
        new_vertices = set(pieces[1].split())

        for vertex in new_vertices:
            edges.append((name, vertex))
            vertex_set.add(vertex)

    vertices = list(vertex_set)

    for pair in edges:
        reverse = (pair[1], pair[0])
        if reverse in edges:
            edges.remove(reverse)

    v = len(vertices)
    e = len(edges)

    graph = Graph(v, e)
    graph.vertices = vertices
    for edge in edges:
        graph.edges.append(Edge(vertices.index(edge[0]), vertices.index(edge[1])))

    cuts, set_counts = karger_min_cut(graph)
    while cuts != 3:
        cuts, set_counts = karger_min_cut(graph)

    print(f'Group sizes: {set_counts}, product: {set_counts[0] * set_counts[1]}\n############################\n')


day_25()

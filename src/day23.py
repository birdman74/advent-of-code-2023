import copy
import os
import random

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day23.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

PATH = '.'
FOREST = '#'


def day_23():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    trail_map = data_file.read().split('\n')

    first_row = trail_map[0]
    height = len(trail_map)
    last_row = trail_map[height - 1]

    start = (first_row.find(PATH), 0)
    end = (last_row.find(PATH), height - 1)

    weighted_map = build_weighted_map(trail_map, start, end)

    most_steps = max_path_length(weighted_map, start, end)

    print(f'Longest hike: {most_steps} steps\n############################\n')


def max_path_length(weighted_map, start, end):
    max_paths = {(start,): 0}

    long_path_length = 0
    while len(max_paths.keys()) > 0:
        new_max_paths = {}
        for path in max_paths.keys():
            path_end = path[-1]
            for vertex in weighted_map[path_end].keys():
                if vertex not in path:
                    new_key = path + (vertex,)
                    new_path_total = max_paths[path] + weighted_map[path_end][vertex]
                    if vertex == end:
                        long_path_length = max(long_path_length, new_path_total)
                    else:
                        new_max_paths[new_key] = new_path_total

        max_paths = new_max_paths
        new_max_paths = {}

    return long_path_length


def find_next_vertex(vertex, branch_point, trail_map, vertices):
    branch_length = 1
    spot = branch_point
    visited = [vertex]
    while True:
        if spot in vertices:
            return branch_length, spot

        next_spots = next_steps(spot, trail_map, visited)
        visited.append(spot)
        spot = next_spots[0]
        branch_length += 1


def build_weighted_map(trail_map, start, end):
    weighted_map = {}
    vertices = [start, end] + find_vertices(trail_map)

    for vertex in vertices:
        weighted_map[vertex] = {}

    for vertex in vertices:
        branch_points = next_steps(vertex, trail_map, [])
        for branch_point in branch_points:
            branch_length, next_vertex = find_next_vertex(vertex, branch_point, trail_map, vertices)

            if next_vertex in weighted_map[vertex].keys():
                branch_length = max(branch_length,weighted_map[vertex][next_vertex])

            weighted_map[vertex][next_vertex] = branch_length
            weighted_map[next_vertex][vertex] = branch_length

    return weighted_map


def find_vertices(trail_map):
    vertices = []
    for y in range(len(trail_map)):
        for x in range(len(trail_map[0])):
            current = (x, y)
            if trail_map[y][x] != FOREST:
                next_spots = next_steps(current, trail_map, [])
                if len(next_spots) > 2:
                    vertices.append(current)

    return vertices


def next_steps(vertex, trail_map, visited_spots):
    (x, y) = vertex
    possible_steps = []
    possibilities = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
    for point in possibilities:
        if inbounds(point, trail_map) and point not in visited_spots and trail_map[point[1]][point[0]] != FOREST:
            possible_steps.append(point)

    return possible_steps


def inbounds(point, trail_map):
    (x, y) = point
    h = len(trail_map)
    w = len(trail_map[0])
    return 0 <= x < w and 0 <= y < h


day_23()

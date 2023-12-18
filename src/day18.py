import os
from enum import Enum

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day18.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


class Dir(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'
    ORIGIN = 'O'


def day_18():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    trench_spots = {(0,0): False}
    x = 0
    y = 0
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0

    for line in lines:
        pieces = line.split()
        direction = Dir(pieces[0])
        length = int(pieces[1])
        for i in range(length):
            x, y = move(x, y, direction)
            new_spot = (x, y)
            if new_spot not in trench_spots.keys():
                trench_spots[new_spot] = False
                min_y = min(min_y, y)
                max_x = max(max_x, x)

    total_volume = len(trench_spots) + inside_spot_count(trench_spots)

    print(f'Total volume: {total_volume}\n############################\n')


def crawl(perimeter, spot):
    spots = {spot: False}
    unvisited = {spot: False}
    visited = {}

    while len(unvisited) > 0:
        new_unvisited = {}
        for x, y in unvisited.keys():
            left = move(x, y, Dir.LEFT)
            if left not in visited.keys() and left not in perimeter.keys():
                visited[left] = False
                new_unvisited[left] = False

            right = move(x, y, Dir.RIGHT)
            if right not in visited.keys() and right not in perimeter.keys():
                visited[right] = False
                new_unvisited[right] = False

            up = move(x, y, Dir.UP)
            if up not in visited.keys() and up not in perimeter.keys():
                visited[up] = False
                new_unvisited[up] = False

            down = move(x, y, Dir.DOWN)
            if down not in visited.keys() and down not in perimeter.keys():
                visited[down] = False
                new_unvisited[down] = False

        unvisited = new_unvisited

    return visited


def inside_spot_count(outside_locations):
    initial_spot = (1, 1)
    if point_inside(outside_locations, (1, -1)):
        initial_spot = (1, -1)

    spots = crawl(outside_locations, initial_spot)
    return len(spots)


def move(x, y, direction):
    match direction:
        case Dir.UP:
            return x, y - 1
        case Dir.DOWN:
            return x, y + 1
        case Dir.LEFT:
            return x - 1, y
        case Dir.RIGHT:
            return x + 1, y


def point_inside(outside_locations, start_point):
    crossings = 0

    x, y = start_point

    y_points = [p for p in outside_locations.keys() if p[0] == x and p[1] > y]
    y_points.sort()

    crossings = 0
    for i in range(len(y_points)):
        y = y_points[i][1]

        if i < len(y_points) - 1 and y_points[i + 1][1] == y + 1:
            continue

        crossings += 1

    return crossings % 2 == 1


day_18()

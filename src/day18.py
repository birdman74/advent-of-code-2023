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

    corners = []
    trench_length = 0

    for line in lines:
        pieces = line.split()
        instructions = pieces[2][2:8]
        length = int(instructions[0:5], 16)
        trench_length += length
        match instructions[5]:
            case '0':
                x += length
            case '1':
                y += length
            case '2':
                x -= length
            case '3':
                y -= length

        corners.append((x, y))

    inner_volume = shoelace(corners)

    total_volume = inner_volume + (trench_length / 2) + 1

    print(f'Total volume: {total_volume}\n############################\n')


def shoelace(corners):
    num_corners = len(corners)
    area = 0.0
    for i in range(num_corners):
        p1 = corners[i]
        p2 = corners[(i + 1) % num_corners]
        area += p1[0] * p2[1]
        area -= p2[0] * p1[1]
    return abs(area) / 2


day_18()

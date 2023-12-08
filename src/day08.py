import os
import numpy

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day08.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

LEFT = 0
RIGHT = 1


def day_08():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    directions = lines[0]
    directions_length = len(directions)
    lr_map = {}

    for i in range(2, len(lines)):
        line = lines[i]
        pieces = line.split(' = ')
        source = pieces[0]
        pieces = pieces[1][1:len(pieces[1]) - 1].split(', ')
        left = pieces[0]
        right = pieces[1]
        lr_map[source] = (left, right)

    sources = [node for node in lr_map.keys() if node.endswith('A')]
    z_distance_lcm = -1

    for source in sources:
        steps = 0
        directions_index = 0
        while not source.endswith('Z'):
            source = lr_map[source][turn(directions[directions_index])]

            directions_index = (directions_index + 1) % directions_length
            steps += 1

        if z_distance_lcm == -1:
            z_distance_lcm = steps
        else:
            z_distance_lcm = numpy.lcm(z_distance_lcm, steps, dtype=object)

    print(f'Number of steps: {z_distance_lcm}\n############################\n')


def turn(direction):
    if direction == 'L':
        return LEFT
    else:
        return RIGHT


day_08()

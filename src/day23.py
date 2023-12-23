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
SLIDE_UP = '^'
SLIDE_DOWN = 'v'
SLIDE_RIGHT = '>'
SLIDE_LEFT = '<'


def day_23():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    trail_map = data_file.read().split('\n')

    start = (trail_map[0].find(PATH), 0)

    most_steps = 0

    hikes = [Hike(start, trail_map)]

    while len(hikes) > 0:
        hikes_to_remove = []
        hikes_to_add = []
        for hike in hikes:
            next_steps = hike.next_steps()
            if len(next_steps) == 0:
                hikes_to_remove.append(hike)
            else:
                for i in range(len(next_steps)):
                    next_step = next_steps[i]
                    if next_step[1] == len(trail_map) - 1:
                        most_steps = max(most_steps, len(hike.visited_spots))
                        hikes_to_remove.append(hike)
                    else:
                        if i < len(next_steps) - 1:
                            hike2 = copy.deepcopy(hike)
                            hike2.move_to(next_step)
                            hikes_to_add.append(hike2)
                        else:
                            hike.move_to(next_step)

        hike_set = set(hikes) - set(hikes_to_remove)
        hike_set.update(set(hikes_to_add))
        hikes = list(hike_set)

    print(f'Longest hike: {most_steps} steps\n############################\n')


class Hike:
    def __init__(self, start_pos, trail_map):
        self.position = start_pos
        self.trail_map = trail_map
        self.visited_spots = [self.position]
        self.trail_height = len(self.trail_map)
        self.trail_width = len(self.trail_map[0])
        self.id = random.randint(0, 1000000)

    def __hash__(self):
        return self.id

    def __repr__(self):
        return f'{self.position}'

    def clone(self):
        h = Hike(self.position, self.trail_map)
        h.visited_spots = copy.deepcopy(self.visited_spots)
        return h

    def next_steps(self):
        (x, y) = self.position
        return_positions = []

        current_spot = self.trail_map[y][x]

        if current_spot == SLIDE_DOWN:
            possible_positions = [(x, y + 1)]
        elif current_spot == SLIDE_LEFT:
            possible_positions = [(x - 1, y)]
        elif current_spot == SLIDE_RIGHT:
            possible_positions = [(x + 1, y)]
        elif current_spot == SLIDE_UP:
            possible_positions = [(x, y - 1)]
        else:
            possible_positions = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]

        for p in possible_positions:
            if p not in self.visited_spots and self.inbounds(p) and self.trail_map[p[1]][p[0]] != FOREST:
                return_positions.append(p)

        return return_positions

    def inbounds(self, p):
        x, y = p
        return 0 <= x < self.trail_width and 0 <= y < self.trail_height

    def move_to(self, new_spot):
        self.position = new_spot
        self.visited_spots.append(new_spot)


day_23()

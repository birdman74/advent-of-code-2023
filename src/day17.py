import os
import functools
from enum import Enum

INPUT_DIR = os.path.join('input', 'samples')
# INPUT_DIR = 'input'

INPUT_FILE = 'day17.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


class Dir(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'
    ORIGIN = 'O'


visited_nodes = {}
loss_map = []


def day_17():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')
    for line in lines:
        loss_map.append([int(c) for c in line])

    finish_coordinates = (len(loss_map[0]) - 1, len(loss_map) - 1)

    walk_map(finish_coordinates)

    total_heat_loss = min([visited_nodes[k] for k in visited_nodes.keys() if k[0] == finish_coordinates])

    print(f'Minimum total heat loss: {total_heat_loss}\n############################\n')


@functools.cache
def heat_loss_at(point):
    (x, y) = point
    return loss_map[y][x]


@functools.cache
def coord_offsets(step_dir):
    match step_dir:
        case Dir.LEFT:
            return -1, 0
        case Dir.RIGHT:
            return 1, 0
        case Dir.UP:
            return 0, -1
        case Dir.DOWN:
            return 0, 1


@functools.cache
def new_position(current, step_dir):
    (x, y) = current
    offsets = coord_offsets(step_dir)
    return x + offsets[0], y + offsets[1]


@functools.cache
def step_is_possible(current, step_dir):
    h = len(loss_map)
    w = len(loss_map[0])

    x, y = new_position(current, step_dir)
    return 0 <= x < w and 0 <= y < h


def walk_map(destination):
    unvisited = {((0, 0), (Dir.ORIGIN,) * 4): 0}
    new_unvisited = {}

    while len(unvisited) > 0:
        current_solutions = [visited_nodes[k] for k in visited_nodes.keys() if k[0] == destination]
        current_best_solution = min(current_solutions) if len(current_solutions) > 0 else 0

        for key in unvisited.keys():
            current = key[0]
            prev_steps = key[1]
            current_heat_loss = unvisited[key]

            moves = next_moves(prev_steps)
            for move in moves:
                if move_is_possible(current, move):
                    new_steps = prev_steps
                    if move[0] == prev_steps[0]:
                        new_steps += move
                    else:
                        new_steps = move
                    new_location = new_position(current, move)
                    new_location_heat_loss = current_heat_loss + heat_loss_thru_move(current, move)
                    if 0 < current_best_solution < new_location_heat_loss:
                        continue
                    visited_key = (new_location, )
                    if visited_key not in visited_nodes.keys() or new_location_heat_loss < visited_nodes[visited_key]:
                        visited_nodes[visited_key] = new_location_heat_loss
                        new_unvisited[visited_key] = new_location_heat_loss

        unvisited = new_unvisited
        new_unvisited = {}
        print(f'new_unvisited length: {len(unvisited)}')


@functools.cache
def next_moves(prev_steps):
    run_length = len(prev_steps)
    current_dir = prev_steps[0]
    new_r = (Dir.RIGHT,) * 4
    new_d = (Dir.DOWN,) * 4
    new_u = (Dir.UP,) * 4
    new_l = (Dir.LEFT,) * 4

    match current_dir:
        case Dir.ORIGIN:
            return new_r, new_d
        case Dir.LEFT:
            if run_length == 10:
                return new_d, new_u
            else:
                return new_d, new_u, (Dir.LEFT,)
        case Dir.RIGHT:
            if run_length == 10:
                return new_d, new_u
            else:
                return new_d, new_u, (Dir.RIGHT,)
        case Dir.UP:
            if run_length == 10:
                return new_r, new_l
            else:
                return new_r, new_l, (Dir.UP,)
        case Dir.DOWN:
            if run_length == 10:
                return new_r, new_l
            else:
                return new_r, new_l, (Dir.DOWN,)


day_17()

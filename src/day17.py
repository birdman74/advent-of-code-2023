import os
import functools
from enum import Enum

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

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


visited_nodes = {((0, 0), (Dir.ORIGIN,)): 0}
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
    unvisited = {((0, 0), (Dir.ORIGIN, Dir.ORIGIN, Dir.ORIGIN)): 0}
    new_unvisited = {}

    while len(unvisited) > 0:
        current_solutions = [visited_nodes[k] for k in visited_nodes.keys() if k[0] == destination]
        current_best_solution = min(current_solutions) if len(current_solutions) > 0 else 0

        for key in unvisited.keys():
            current = key[0]
            prev_steps = key[1]
            current_heat_loss = unvisited[key]

            updated_step_combos = step_combos(prev_steps, 1)
            for step_combo in updated_step_combos:
                step = step_combo[2]
                if step_is_possible(current, step):
                    new_location = new_position(current, step)
                    new_location_heat_loss = current_heat_loss + heat_loss_at(new_location)
                    if 0 < current_best_solution < new_location_heat_loss:
                        continue
                    visited_key = (new_location, step_combo)
                    if visited_key not in visited_nodes.keys() or new_location_heat_loss < visited_nodes[visited_key]:
                        visited_nodes[visited_key] = new_location_heat_loss
                        new_unvisited[visited_key] = new_location_heat_loss

        unvisited = new_unvisited
        new_unvisited = {}
        print(f'new_unvisited length: {len(unvisited)}')


@functools.cache
def step_combos(prev_steps, num_steps):
    if num_steps == 1:
        prev_two = prev_steps[1:]
        with_d = prev_two + (Dir.DOWN,)
        with_u = prev_two + (Dir.UP,)
        with_l = prev_two + (Dir.LEFT,)
        with_r = prev_two + (Dir.RIGHT,)
        prev_all_same = len(set(prev_steps)) == 1
        match prev_steps[-1]:
            case Dir.ORIGIN:
                return with_r, with_d
            case Dir.LEFT:
                if prev_all_same:
                    return with_d, with_u
                else:
                    return with_d, with_u, with_l
            case Dir.RIGHT:
                if prev_all_same:
                    return with_d, with_u
                else:
                    return with_r, with_d, with_u
            case Dir.UP:
                if prev_all_same:
                    return with_r, with_l
                else:
                    return with_r, with_u, with_l
            case Dir.DOWN:
                if prev_all_same:
                    return with_r, with_l
                else:
                    return with_r, with_d, with_l
    else:
        step_sets = step_combos(prev_steps, 1)
        new_results = ()
        for new_steps in step_sets:
            new_results += step_combos(new_steps, num_steps - 1)

        return tuple(set(new_results))


day_17()

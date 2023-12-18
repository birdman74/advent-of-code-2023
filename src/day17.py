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

    total_heat_loss = minimum_total_heat_loss((0, 0),
                                              finish_coordinates,
                                              (Dir.ORIGIN, Dir.ORIGIN, Dir.ORIGIN),
                                              0)

    # 637 too high

    print(f'Minimum total heat loss: {total_heat_loss}\n############################\n')


@functools.cache
def calc_heat_loss_for_steps(point, steps):
    total_loss = 0
    x = point[0]
    y = point[1]
    for step in steps:
        offsets = coord_offsets(step)
        x += offsets[0]
        y += offsets[1]
        total_loss += loss_map[y][x]
    return total_loss


@functools.cache
def coord_offsets(dir):
    match dir:
        case Dir.LEFT:
            return -1, 0
        case Dir.RIGHT:
            return 1, 0
        case Dir.UP:
            return 0, -1
        case Dir.DOWN:
            return 0, 1


@functools.cache
def new_position(current, combo):
    x = current[0]
    y = current[1]
    for step in combo:
        offsets = coord_offsets(step)
        x += offsets[0]
        y += offsets[1]
    return x, y


@functools.cache
def combo_is_possible(current, combo, map_h, map_w):
    for i in range(len(combo)):
        sub_combo = combo[0:i+1]
        x, y = new_position(current, sub_combo)
        if not (0 <= x < map_w and 0 <= y < map_h):
            return False
    return True


@functools.cache
def minimum_total_heat_loss(current, destination, prev_dirs, current_heat_loss):
    three_step_combos = step_combos(prev_dirs, 3)
    x = current[0]
    y = current[1]
    h = len(loss_map)
    w = len(loss_map[0])

    for combo in three_step_combos:
        if combo_is_possible(current, combo, h, w):
            new_location = new_position(current, combo)
            if next != (0, 0):
                new_location_heat_loss = current_heat_loss + calc_heat_loss_for_steps(current, combo)
                visited_key = (new_location, combo)
                if visited_key not in visited_nodes.keys() or new_location_heat_loss < visited_nodes[visited_key]:
                    visited_nodes[visited_key] = new_location_heat_loss


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

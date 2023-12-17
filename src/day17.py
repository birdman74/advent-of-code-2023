import os
import functools
from enum import Enum

INPUT_DIR = os.path.join('input', 'samples')
# INPUT_DIR = 'input'

INPUT_FILE = 'day17.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'
    ORIGIN = 'O'


visited_nodes = {((0, 0), (Direction.ORIGIN,)): 0}
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
                                              (Direction.ORIGIN, Direction.ORIGIN, Direction.ORIGIN))

    # 637 too high

    print(f'Minimum total heat loss: {total_heat_loss}\n############################\n')


@functools.cache
def minimum_total_heat_loss(current, destination, prev_dirs):
    directions = new_directions(prev_dirs)
    prev_two_dir = prev_dirs[1:3]
    x = current[0]
    y = current[1]
    h = len(loss_map)
    w = len(loss_map[0])
    current_pos_heat_loss = loss_map[y][x]

    current_low = -1
    for direction in directions:
        match direction:
            case Direction.LEFT:
                new_x = x - 1
                new_y = y
                new_direction = Direction.LEFT
            case Direction.RIGHT:
                new_x = x + 1
                new_y = y
                new_direction = Direction.RIGHT
            case Direction.UP:
                new_x = x
                new_y = y - 1
                new_direction = Direction.UP
            case _:
                new_x = x
                new_y = y + 1
                new_direction = Direction.DOWN

        if 0 <= new_x < w and 0 <= new_y < h:
            new_coords = (new_x, new_y)
            if new_coords == destination:
                return current_pos_heat_loss + loss_map[destination[1]][destination[0]]

            new_dir_tuple = (*prev_two_dir, new_direction)

            new_destination_loss = minimum_total_heat_loss(new_coords, destination, new_dir_tuple)

            if new_destination_loss != -1:
                if current_low == -1:
                    current_low = new_destination_loss
                else:
                    current_low = min(current_low, new_destination_loss)

    if current_low == -1:
        return current_low
    else:
        return current_low + current_pos_heat_loss


@functools.cache
def new_directions(previous_directions):
    if len(set(previous_directions)) == 1:
        match previous_directions[0]:
            case Direction.LEFT | Direction.RIGHT:
                return Direction.DOWN, Direction.UP
            case _:
                return Direction.RIGHT, Direction.LEFT
    else:
        match previous_directions[2]:
            case Direction.LEFT:
                return Direction.DOWN, Direction.LEFT, Direction.UP
            case Direction.RIGHT:
                return Direction.RIGHT, Direction.DOWN, Direction.UP
            case Direction.UP:
                return Direction.RIGHT, Direction.LEFT, Direction.UP
            case _:
                return Direction.RIGHT, Direction.DOWN, Direction.LEFT


day_17()

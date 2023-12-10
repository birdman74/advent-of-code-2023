import os
from enum import Enum

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day10.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

START = 'S'


def day_10():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    pipe_map = data_file.read().split('\n')

    starting_point = find_starting_point(pipe_map)
    move_positions = starting_point.move_next()

    moves = 1

    while move_positions[0] != move_positions[1]:
        move_positions[0] = move_positions[0].move_next()[0]
        move_positions[1] = move_positions[1].move_next()[0]
        moves += 1

    print(f'Number of moves: {moves}\n############################\n')


def find_starting_point(pipe_map):
    for y in range(len(pipe_map)):
        line = pipe_map[y]
        x = line.find(START)
        if x > -1:
            return PointDay10(x, y, pipe_map, Direction.ORIGIN)


class PointDay10:
    def __init__(self, x, y, pipe_map, from_direction):
        self.x = x
        self.y = y
        self.pipe_map = pipe_map
        self.from_direction = from_direction

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __eq__(self, other):
        if not isinstance(other, PointDay10):
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def move_next(self):
        possible_moves = []
        try:
            possible_moves.append(self.left())
        except IndexError:
            pass

        try:
            possible_moves.append(self.up())
        except IndexError:
            pass

        try:
            possible_moves.append(self.right())
        except IndexError:
            pass

        try:
            possible_moves.append(self.down())
        except IndexError:
            pass

        return possible_moves

    def left(self):
        new_x = self.x - 1

        if (self.from_direction == Direction.WEST or self.x == 0 or
                PipeType(self.pipe_map[self.y][self.x]) in
                [PipeType.VERTICAL, PipeType.NEL, PipeType.SEL] or
                PipeType(self.pipe_map[self.y][new_x]) in
                [PipeType.VERTICAL, PipeType.NWL, PipeType.SWL, PipeType.GROUND]):
            raise IndexError("Can't move left")

        return PointDay10(new_x, self.y, self.pipe_map, Direction.EAST)

    def right(self):
        new_x = self.x + 1

        if (self.from_direction == Direction.EAST or self.x == len(self.pipe_map[0]) - 1 or
                PipeType(self.pipe_map[self.y][self.x]) in
                [PipeType.VERTICAL, PipeType.NWL, PipeType.SWL] or
                PipeType(self.pipe_map[self.y][new_x]) in
                [PipeType.VERTICAL, PipeType.NEL, PipeType.SEL, PipeType.GROUND]):
            raise IndexError("Can't move right")

        return PointDay10(self.x + 1, self.y, self.pipe_map, Direction.WEST)

    def up(self):
        new_y = self.y - 1

        if (self.from_direction == Direction.NORTH or self.y == 0 or
                PipeType(self.pipe_map[self.y][self.x]) in
                [PipeType.HORIZONTAL, PipeType.SEL, PipeType.SWL] or
                PipeType(self.pipe_map[new_y][self.x]) in
                [PipeType.HORIZONTAL, PipeType.NEL, PipeType.NWL, PipeType.GROUND]):
            raise IndexError("Can't move up")

        return PointDay10(self.x, self.y - 1, self.pipe_map, Direction.SOUTH)

    def down(self):
        new_y = self.y + 1

        if (self.from_direction == Direction.SOUTH or self.y == len(self.pipe_map) - 1 or
                PipeType(self.pipe_map[self.y][self.x]) in
                [PipeType.HORIZONTAL, PipeType.NWL, PipeType.NEL] or
                PipeType(self.pipe_map[new_y][self.x]) in
                [PipeType.HORIZONTAL, PipeType.SWL, PipeType.SEL, PipeType.GROUND]):
            raise IndexError("Can't move down")

        return PointDay10(self.x, self.y + 1, self.pipe_map, Direction.NORTH)


class PipeType(Enum):
    VERTICAL = '|'
    HORIZONTAL = '-'
    NEL = 'L'
    NWL = 'J'
    SWL = '7'
    SEL = 'F'
    GROUND = '.'
    ANIMAL = START


class Direction(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'
    ORIGIN = '*'


day_10()

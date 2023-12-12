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

    pipe_locations = {}
    starting_point = find_starting_point(pipe_map)
    pipe_locations[starting_point.x, starting_point.y] = starting_point

    move_positions = starting_point.next_moves()

    while move_positions[0] != move_positions[1]:
        for p in move_positions:
            pipe_locations[(p.x, p.y)] = p
        move_positions[0] = move_positions[0].next_moves()[0]
        move_positions[1] = move_positions[1].next_moves()[0]

    furthest_point = move_positions[0]
    pipe_locations[(furthest_point.x, furthest_point.y)] = furthest_point

    nesting_point_count = 0

    for x in range(len(pipe_map[0])):
        for y in range(len(pipe_map)):
            if nesting_point((x, y), pipe_locations):
                nesting_point_count += 1

    print(f'Number of nesting points: {nesting_point_count}\n############################\n')


def nesting_point(p, pipe_locations):
    if p in pipe_locations.keys():
        return False

    left_crosses = shoot_ray_left(pipe_locations, p)
    if left_crosses > 0:
        return left_crosses % 2 == 1

    return False


def shoot_ray_left(pipe_locations, start_point):
    combos = [[PointType.SWL, PointType.NEL], [PointType.NWL, PointType.SEL]]
    combo_index = -1

    crossings = 0

    y = start_point[1]
    for x in range(start_point[0] - 1, -1, -1):
        point = (x, y)

        if point in pipe_locations.keys():
            p = pipe_locations[point]
            if p.point_type == PointType.VERTICAL:
                crossings += 1
                combo_index = -1
            elif p.point_type == combos[0][0]:
                combo_index = 0
            elif p.point_type == combos[1][0]:
                combo_index = 1
            elif combo_index >= 0 and p.point_type == combos[combo_index][1]:
                crossings += 1
                combo_index = -1
            elif p.point_type != PointType.HORIZONTAL:
                combo_index = -1

    return crossings


def find_starting_point(pipe_map):
    for y in range(len(pipe_map)):
        line = pipe_map[y]
        x = line.find(START)
        if x > -1:
            return PointDay10(x, y, pipe_map, Direction.NOWHERE)


class PointDay10:
    def __init__(self, x, y, pipe_map, from_direction, point_type=None):
        self.x = x
        self.y = y
        self.pipe_map = pipe_map
        self.from_direction = from_direction
        self.point_type = PointType(pipe_map[y][x])

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __eq__(self, other):
        if not isinstance(other, PointDay10):
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def next_moves(self):
        possible_moves = []
        directions = []
        try:
            possible_moves.append(self.left())
            directions.append(Direction.WEST)
        except IndexError:
            pass

        try:
            possible_moves.append(self.up())
            directions.append(Direction.NORTH)
        except IndexError:
            pass

        try:
            possible_moves.append(self.right())
            directions.append(Direction.EAST)
        except IndexError:
            pass

        try:
            possible_moves.append(self.down())
            directions.append(Direction.SOUTH)
        except IndexError:
            pass

        if self.point_type == PointType.ANIMAL:
            if Direction.WEST in directions:
                if Direction.EAST in directions:
                    self.point_type = PointType.HORIZONTAL
                elif Direction.NORTH in directions:
                    self.point_type = PointType.NWL
                else:
                    self.point_type = PointType.SWL
            elif Direction.NORTH in directions:
                if Direction.SOUTH in directions:
                    self.point_type = PointType.VERTICAL
                else:
                    self.point_type = PointType.NEL
            else:
                self.point_type = PointType.SEL

        return possible_moves

    def left(self):
        new_x = self.x - 1

        if (self.from_direction == Direction.WEST or self.x == 0 or
                PointType(self.pipe_map[self.y][self.x]) in
                [PointType.VERTICAL, PointType.NEL, PointType.SEL] or
                PointType(self.pipe_map[self.y][new_x]) in
                [PointType.VERTICAL, PointType.NWL, PointType.SWL, PointType.GROUND]):
            raise IndexError("Can't move left")

        return PointDay10(new_x, self.y, self.pipe_map, Direction.EAST)

    def right(self):
        new_x = self.x + 1

        if (self.from_direction == Direction.EAST or self.x == len(self.pipe_map[0]) - 1 or
                PointType(self.pipe_map[self.y][self.x]) in
                [PointType.VERTICAL, PointType.NWL, PointType.SWL] or
                PointType(self.pipe_map[self.y][new_x]) in
                [PointType.VERTICAL, PointType.NEL, PointType.SEL, PointType.GROUND]):
            raise IndexError("Can't move right")

        return PointDay10(self.x + 1, self.y, self.pipe_map, Direction.WEST)

    def up(self):
        new_y = self.y - 1

        if (self.from_direction == Direction.NORTH or self.y == 0 or
                PointType(self.pipe_map[self.y][self.x]) in
                [PointType.HORIZONTAL, PointType.SEL, PointType.SWL] or
                PointType(self.pipe_map[new_y][self.x]) in
                [PointType.HORIZONTAL, PointType.NEL, PointType.NWL, PointType.GROUND]):
            raise IndexError("Can't move up")

        return PointDay10(self.x, self.y - 1, self.pipe_map, Direction.SOUTH)

    def down(self):
        new_y = self.y + 1

        if (self.from_direction == Direction.SOUTH or self.y == len(self.pipe_map) - 1 or
                PointType(self.pipe_map[self.y][self.x]) in
                [PointType.HORIZONTAL, PointType.NWL, PointType.NEL] or
                PointType(self.pipe_map[new_y][self.x]) in
                [PointType.HORIZONTAL, PointType.SWL, PointType.SEL, PointType.GROUND]):
            raise IndexError("Can't move down")

        return PointDay10(self.x, self.y + 1, self.pipe_map, Direction.NORTH)


# Tunnels: ||, 7F, JL, -/-, L/F, J/7
class PointType(Enum):
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
    NOWHERE = '*'


day_10()

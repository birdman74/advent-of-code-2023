import os
import functools

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day22.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

X = 'X'
Y = 'Y'
Z = 'Z'


def day_22():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    brick_map = data_file.read().split('\n')

    bricks = []
    max_x = 0
    max_y = 0
    max_z = 0

    for brick in brick_map:
        pieces = brick.split('~')

        coords = list(map(int, pieces[0].split(',')))
        start = Point22(coords)

        coords = list(map(int, pieces[1].split(',')))
        max_x = max(max_x, coords[0])
        max_y = max(max_y, coords[1])
        max_z = max(max_z, coords[2])
        end = Point22(coords)

        bricks.append(Brick(start, end))

    seated_bricks = {}

    ordered_bricks = {}
    for z in range(1, max_z + 1):
        ordered_bricks[z] = []
        for brick in bricks:
            if z in brick.dims[Z] and not z in ordered_bricks.values():
                ordered_bricks[z].append(brick)

    for z in sorted(ordered_bricks):
        lowest_bricks = ordered_bricks[z]
        for b in lowest_bricks:
            b.drop(seated_bricks)

    sum_of_fallen_bricks = 0

    bricks.reverse()
    for b in bricks:
        sum_of_fallen_bricks += all_fall_down_count(b)

    print(f'Sum of fallen bricks: {sum_of_fallen_bricks}\n############################\n')


@functools.cache
def all_fall_down_count(brick):
    if len(brick.toppers) == 0:
        return 0

    bricks_to_evaluate = brick.all_toppers()

    removed_bricks = {brick}
    newly_removed_brick_count = 1
    while newly_removed_brick_count > 0:
        newly_removed_brick_count = 0

        for b in bricks_to_evaluate:
            if b.supporters.issubset(removed_bricks):
                removed_bricks.add(b)
                newly_removed_brick_count += 1

        bricks_to_evaluate = bricks_to_evaluate.difference(removed_bricks)

    return len(removed_bricks) - 1


def calc_dimensions(start, end):
    return {X: range(start.x, end.x + 1),
            Y: range(start.y, end.y + 1),
            Z: range(start.z, end.z + 1)}


class Brick:
    def __init__(self, start, end):
        self.dims = calc_dimensions(start, end)
        self.toppers = set()
        self.supporters = set()

    def __repr__(self):
        return f'x: {self.dims[X]}, y: {self.dims[Y]}, z: {self.dims[Z]}'

    def __hash__(self):
        return hash(self.dims[X]) + (7 * hash(self.dims[Y])) + (47 * hash(self.dims[Z]))

    @functools.cache
    def all_toppers(self):
        full_toppers = self.toppers.copy()
        for t in self.toppers:
            new_toppers = t.all_toppers()
            full_toppers.update(new_toppers)

        return full_toppers

    def drop(self, seated_bricks):
        low_z = min(self.dims[Z])
        z_floor = 0
        for z_level in range(low_z - 1, -1, -1):
            for x in self.dims[X]:
                for y in self.dims[Y]:
                    if (x, y, z_level) in seated_bricks.keys():
                        z_floor = z_level
                        break
                if z_floor > 0:
                    break
            if z_floor > 0:
                break

        self.rest_at(z_floor, seated_bricks)

    def rest_at(self, z_floor, seated_bricks):
        r = self.dims[Z]
        self.dims[Z] = range(z_floor + 1, z_floor + 1 + (r.stop - r.start))
        for x in self.dims[X]:
            for y in self.dims[Y]:
                if (x, y, z_floor) in seated_bricks.keys():
                    b = seated_bricks[(x, y, z_floor)]
                    b.toppers.add(self)
                    self.supporters.add(b)

                for z in self.dims[Z]:
                    seated_bricks[(x, y, z)] = self


class Point22:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'


day_22()

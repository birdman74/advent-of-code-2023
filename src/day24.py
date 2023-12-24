import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day24.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

# FIELD_MINIMUM = 7
# FIELD_MAXIMUM = 27
FIELD_MINIMUM = 200000000000000
FIELD_MAXIMUM = 400000000000000


def day_24():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    stone_data = data_file.read().split('\n')

    stones = []
    velocities = []
    ms = []
    bs = []
    y_ranges = []

    for data in stone_data:
        pieces = data.split(' @ ')
        stone = tuple(list(map(int, pieces[0].strip().split(', ')))[0:2])
        velocity = tuple(list(map(int, pieces[1].strip().split(', ')))[0:2])
        b = stone[1] - ((velocity[1] / velocity[0]) * stone[0])
        stones.append(stone)
        velocities.append(velocity)
        ms.append(velocity[1] / velocity[0])
        bs.append(b)
        y_ranges.append(y_range(velocity, b, FIELD_MINIMUM, FIELD_MAXIMUM))

        # print(f'({x}, {y}, {z}) at velocity ({xv}, {yv}, {zv})')

    intersect_count = 0

    for i in range(len(bs)):
        for j in range(i + 1, len(bs)):
            if intersect(bs[i], ms[i], bs[j], ms[j],
                         stones[i][0], velocities[i][0], stones[j][0], velocities[j][0]):
                intersect_count += 1

    print(f'Number of intersections between X({FIELD_MINIMUM} -> {FIELD_MAXIMUM}): {intersect_count}\n############################\n')


def intersect(b1, m1, b2, m2, x1_now, x1v, x2_now, x2v):
    if m1 == m2:
        return False

    x_at_intersect = (b2 - b1) / (m1 - m2)
    y_at_intersect = m1 * x_at_intersect + b1
    if FIELD_MINIMUM <= x_at_intersect <= FIELD_MAXIMUM and FIELD_MINIMUM <= y_at_intersect <= FIELD_MAXIMUM:
        # past intersection
        if ((x1_now < x_at_intersect and x1v < 0) or (x1_now > x_at_intersect and x1v > 0) or
                ((x2_now < x_at_intersect and x2v < 0) or (x2_now > x_at_intersect and x2v > 0))):
            return False
        else:
            return True
    else:
        return False


def y_range(vel, b, x1, x2):
    return calc_y(vel, b, x1), calc_y(vel, b, x2)


def calc_y(vel, b, x):
    return (vel[1] / vel[0]) * x + b


day_24()

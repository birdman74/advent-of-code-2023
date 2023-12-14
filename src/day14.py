import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day14.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

ROLLER = 'O'
BLOCKER = '#'
CYCLES = 1000000000


def day_14():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    rollers = cycle(lines, CYCLES)

    print(f'Total load: {calculate_load(lines, rollers)}\n############################\n')


def calculate_load(field, rollers):
    load = 0
    max_load = len(field)

    for roller in rollers:
        load += max_load - roller[1]

    return load


def cycle(lines, cycles):
    width = len(lines[0])
    height = len(lines)

    rollers = []
    blockers = []
    for y in range(height):
        for x in range(width):
            if lines[y][x] == ROLLER:
                rollers.append((x, y))
            elif lines[y][x] == BLOCKER:
                blockers.append((x, y))

    def tilt_north():
        move_on_y(range(height))

    def tilt_south():
        move_on_y(range(height - 1, -1, -1))

    def tilt_west():
        move_on_x(range(width))

    def tilt_east():
        move_on_x(range(width - 1, -1, -1))

    def move_on_y(r):
        for x2 in range(width):
            end_y = r.start
            for y2 in r:
                pos = (x2, y2)
                if pos in rollers:
                    rollers.remove(pos)
                    rollers.append((x2, end_y))
                    end_y += r.step
                elif pos in blockers:
                    end_y = y2 + r.step

    def move_on_x(r):
        for y2 in range(height):
            end_x = r.start
            for x2 in r:
                pos = (x2, y2)
                if pos in rollers:
                    rollers.remove(pos)
                    rollers.append((end_x, y2))
                    end_x += r.step
                elif pos in blockers:
                    end_x = x2 + r.step

    def pattern_length(seq):
        k = 1
        repeat_length = 0
        seq_len = len(seq)
        while k < seq_len / 2:
            start = seq_len - (2 * k)
            end = start + k
            if seq[-1 * k:] == seq[start:end]:
                repeat_length = k
            k += 1

        return repeat_length

    loads = []
    max_pattern_length = 0
    looping = False
    for i in range(cycles):
        tilt_north()
        tilt_west()
        tilt_south()
        tilt_east()

        load = calculate_load(lines, rollers)
        print(f'Load after {i} cycles: {load}')
        loads.append(load)

        new_pattern_length = pattern_length(loads)
        if new_pattern_length > max_pattern_length:
            max_pattern_length = new_pattern_length
        elif max_pattern_length > 2 and new_pattern_length == max_pattern_length:
            looping = True

        if looping:
            offset = len(loads) % max_pattern_length
            if (cycles - offset) % max_pattern_length == 0:
                return rollers

    return rollers


def column(field, index):
    return [line[index] for line in field]


day_14()

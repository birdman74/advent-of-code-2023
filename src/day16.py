import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day16.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


def day_16():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    field = data_file.read().split('\n')

    height = len(field)
    width = len(field[0])

    max_energy = 0
    for i in range(height):
        max_energy = max(max_energy, find_energy_total(field, 0, i, Direction.RIGHT))
        max_energy = max(max_energy, find_energy_total(field, width - 1, i, Direction.LEFT))

    for i in range(width):

        max_energy = max(max_energy, find_energy_total(field, i, 0, Direction.DOWN))
        max_energy = max(max_energy, find_energy_total(field, i, height - 1, Direction.UP))

    print(f'Maximum energized tile count: {max_energy}\n############################\n')


def find_energy_total(field, x, y, direction):
    energized_tiles = {(x, y): True}
    # print((x, y))
    beams = {(x, y, direction): False}
    while False in beams.values():
        move_beams(field, beams, energized_tiles)
    return len(energized_tiles)


def move_beams(field, beams, energized_tiles):
    h = len(field)
    w = len(field[0])
    unprocessed_beams = [k for k in beams.keys() if not beams[k]]

    for beam in unprocessed_beams:
        beams[beam] = True

        match field[beam[1]][beam[0]]:
            case SpaceType.SPACE:
                just_move(beam, beams, h, w, energized_tiles)
            case SpaceType.MIRROR_FS:
                mirror_fs(beam, beams, h, w, energized_tiles)
            case SpaceType.MIRROR_BS:
                mirror_bs(beam, beams, h, w, energized_tiles)
            case SpaceType.SPLITTER_H:
                split_h(beam, beams, h, w, energized_tiles)
            case SpaceType.SPLITTER_V:
                split_v(beam, beams, h, w, energized_tiles)


def just_move(b, beams, h, w, e_tiles):
    x, y, direction = b

    match direction:
        case Direction.UP:
            y -= 1
        case Direction.DOWN:
            y += 1
        case Direction.LEFT:
            x -= 1
        case Direction.RIGHT:
            x += 1

    add_new_beam(beams, (x, y, direction), h, w, e_tiles)


def add_new_beam(beams, new_beam, h, w, e_tiles):
    x, y, _ = new_beam
    if 0 <= x < w and 0 <= y < h:
        if new_beam not in beams.keys():
            beams[new_beam] = False
        e_tiles[(x, y)] = True


def mirror_fs(b, beams, h, w, e_tiles):
    x, y, direction = b

    match direction:
        case Direction.UP:
            x += 1
            direction = Direction.RIGHT
        case Direction.DOWN:
            x -= 1
            direction = Direction.LEFT
        case Direction.LEFT:
            y += 1
            direction = Direction.DOWN
        case Direction.RIGHT:
            y -= 1
            direction = Direction.UP

    add_new_beam(beams, (x, y, direction), h, w, e_tiles)


def mirror_bs(b, beams, h, w, e_tiles):
    x, y, direction = b

    match direction:
        case Direction.UP:
            x -= 1
            direction = Direction.LEFT
        case Direction.DOWN:
            x += 1
            direction = Direction.RIGHT
        case Direction.LEFT:
            y -= 1
            direction = Direction.UP
        case Direction.RIGHT:
            y += 1
            direction = Direction.DOWN

    add_new_beam(beams, (x, y, direction), h, w, e_tiles)


def split_h(b, beams, h, w, e_tiles):
    x, y, direction = b

    match direction:
        case Direction.UP | Direction.DOWN:
            new_bs = [(x - 1, y, Direction.LEFT), (x + 1, y, Direction.RIGHT)]
            for b in new_bs:
                add_new_beam(beams, b, h, w, e_tiles)
        case _:
            just_move(b, beams, h, w, e_tiles)


def split_v(b, beams, h, w, e_tiles):
    x, y, direction = b

    match direction:
        case Direction.LEFT | Direction.RIGHT:
            new_bs = [(x, y - 1, Direction.UP), (x, y + 1, Direction.DOWN)]
            for b in new_bs:
                add_new_beam(beams, b, h, w, e_tiles)
        case _:
            just_move(b, beams, h, w, e_tiles)


class SpaceType:
    SPACE = '.'
    MIRROR_FS = '/'
    MIRROR_BS = '\\'
    SPLITTER_H = '-'
    SPLITTER_V = '|'


class Direction:
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'


day_16()

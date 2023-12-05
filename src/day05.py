import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day05.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


def day_05():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    sources = list(map(int, lines[0].split(': ')[1].split(' ')))

    # <dest range> <source range> <range len>

    map_index = 0
    maps = []

    for i in range(len(lines)):
        line = lines[i]
        if line.endswith('map:'):
            i += 1
            line = lines[i]
            while len(line) > 0:
                maps.append(process_map_entry(line))
                i += 1
                if i >= len(lines):
                    break
                line = lines[i]
            # print(maps)
            for j in range(len(sources)):
                sources[j] = find_destination(sources[j], maps)

        maps = []

    nearest_location = min(sources)

    print(f'Nearest location: {nearest_location}\n############################\n')


def find_destination(source, maps):
    for destination_map in maps:
        if source in range(destination_map[0], destination_map[0] + destination_map[1]):
            return source + destination_map[2]

    return source


def process_map_entry(line):
    nums = list(map(int, line.split(' ')))
    return nums[1], nums[2], nums[0] - nums[1]


day_05()

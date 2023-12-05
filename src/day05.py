import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day05.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

ORIGINAL_MAP_DEST_INDEX = 0
ORIGINAL_MAP_SRC_INDEX = 1
ORIGINAL_MAP_RANGE_INDEX = 2

MAP_SRC_INDEX = 0
MAP_RANGE_INDEX = 1
MAP_OFFSET_INDEX = 2

SRC_START_INDEX = 0
SRC_RANGE_INDEX = 1


def day_05():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    sources = list(map(int, lines[0].split(': ')[1].split(' ')))
    source_ranges = []
    for i in range(0, len(sources), 2):
        source_ranges.append((sources[i], sources[i + 1]))

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

            new_source_ranges = []
            for j in range(len(source_ranges)):
                new_source_ranges.extend(find_destinations(source_ranges[j], maps))

            source_ranges = new_source_ranges

        maps = []

    nearest_location = min([loc[0] for loc in source_ranges])

    print(f'Nearest location: {nearest_location}\n############################\n')


def find_destinations(source_range, maps):
    unmapped_ranges = [(source_range[0], source_range[1])]  # copy param
    dest_ranges = []
    new_unmapped_ranges = []

    for current_map in maps:
        map_start = current_map[MAP_SRC_INDEX]
        map_end = map_start + current_map[MAP_RANGE_INDEX] - 1
        offset = current_map[MAP_OFFSET_INDEX]

        for i in range(len(unmapped_ranges) - 1, -1, -1):
            unmapped_range = unmapped_ranges[i]
            unmapped_ranges.remove(unmapped_range)

            src_start = unmapped_range[SRC_START_INDEX]
            src_end = src_start + unmapped_range[SRC_RANGE_INDEX] - 1

            if src_end < map_start or src_start > map_end:
                # no overlap, no mappings exist
                # ssss                     ssss
                #      mmmm   OR      mmmm
                new_unmapped_ranges.append(unmapped_range)
            elif map_start <= src_start and src_end <= map_end:
                # complete overlap, map all values
                #        sssss
                #     mmmmmmmmmmmmmmm
                dest_ranges.append((src_start + offset, unmapped_range[SRC_RANGE_INDEX]))
            elif map_start <= src_end <= map_end:
                # result: initial range of unmapped values + remaining range of mapped values
                #                 sssssssssssssss
                #                          mmmmmmmmmmmmm
                # unmapped :      sssssssss
                # mapped :                 nnnnnn
                new_unmapped_ranges.append((src_start, map_start - src_start))
                dest_ranges.append((map_start + offset, src_end - map_start + 1))
            elif map_start <= src_start <= map_end:
                # result: initial range of mapped values + remainder  of unmapped values
                #                         ssssssssss
                #            mmmmmmmmmmmmmmmmmmm
                # unmapped:                     sssss
                # mapped:                  nnnnn
                dest_ranges.append((src_start + offset, map_end - src_start + 1))
                new_unmapped_ranges.append((map_end + 1, src_end - map_end))
            else:
                # result: initial range of unmapped, range of mapped, remainder of unmapped values
                #             sssssssssssssssssssssssssssss
                #                       mmmmmmmm
                # unmapped:   ssssssssss        sssssssssss
                # mapped:               nnnnnnnn
                new_unmapped_ranges.append((src_start, map_start - src_start))
                dest_ranges.append((map_start + offset, offset))
                new_unmapped_ranges.append((map_end + 1, src_end - map_end))

            unmapped_ranges = new_unmapped_ranges

    if len(dest_ranges) == 0:
        return [source_range]

    if len(new_unmapped_ranges) > 0:
        dest_ranges.extend(new_unmapped_ranges)

    return dest_ranges


def process_map_entry(line):
    nums = list(map(int, line.split(' ')))
    return nums[ORIGINAL_MAP_SRC_INDEX], nums[ORIGINAL_MAP_RANGE_INDEX], nums[ORIGINAL_MAP_DEST_INDEX] - nums[ORIGINAL_MAP_SRC_INDEX]


day_05()

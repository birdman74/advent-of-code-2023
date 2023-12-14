import os
import functools

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day12.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'
OPERATIONAL_MATCHES = '.?'
DAMAGED_MATCHES = '#?'


def day_12():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    total = 0
    i = 1

    for line in lines:
        pieces = line.split(' ')
        springs = pieces[0]
        springs = 4 * (springs + UNKNOWN) + springs
        nums = list(map(int, (4 * (pieces[1] + ',') + pieces[1]).split(',')))

        print(f'{i}. {springs} {nums}')

        arrangement_count = possible_arrangements(springs, tuple(nums))
        print(f'\tArrangement count: {arrangement_count}')

        total += arrangement_count
        i += 1

    print(f'Total Arrangements: {total}\n############################\n')


@functools.cache
def possible_arrangements(springs, damaged_nums):
    count = 0
    first_span = damaged_nums[0]
    min_length = min_array_length(damaged_nums)

    for i in range(0, len(springs) - min_length + 1):
        if springs[0:i].find(DAMAGED) > -1:
            return count

        sub = springs[i:i + first_span]
        remainder = springs[i + first_span:]
        if len(damaged_nums) == 1 and remainder.find(DAMAGED) > - 1:
            continue

        if len(sub) == first_span and set(sub) <= set(DAMAGED_MATCHES):
            surrounds = ''
            if i > 0:
                surrounds = springs[i - 1]
            if i < len(springs) - len(sub):
                surrounds += springs[i + len(sub)]

            if set(surrounds) <= set(OPERATIONAL_MATCHES):
                new_start = i + len(sub) + 1
                new_damaged_nums = damaged_nums[1:]

                if new_start >= len(springs) or len(new_damaged_nums) == 0:
                    count += 1
                else:
                    count += possible_arrangements(springs[new_start:], new_damaged_nums)

        if sub[0] == DAMAGED:
            return count

    return count


def min_array_length(groups):
    return sum(groups) + len(groups) - 1


day_12()

import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day09.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


def day_09():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    next_in_series_sum = 0
    previous_in_series_sum = 0

    for line in lines:
        nums = list(map(int, line.split(' ')))

        (previous_in_series, next_in_series) = previous_and_next_in_series(nums)

        previous_in_series_sum += previous_in_series
        next_in_series_sum += next_in_series

    print(f'Previous-in-Series sum: {previous_in_series_sum}\n############################\n')
    print(f'Next-in-Series sum: {next_in_series_sum}\n############################\n')


def previous_and_next_in_series(series):
    new_series = []
    for i in range(0, len(series) - 1):
        new_series.append(series[i + 1] - series[i])

    if len([x for x in new_series if x == 0]) == len(new_series):
        return series[0], series[-1]
    else:
        (previous_in_series, next_in_series) = previous_and_next_in_series(new_series)
        return series[0] - previous_in_series, series[-1] + next_in_series


day_09()

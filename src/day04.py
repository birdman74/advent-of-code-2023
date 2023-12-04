import os

INPUT_DIR = 'input'
# INPUT_DIR = os.path.join('input', 'samples')

INPUT_FILE = 'day04.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


def day_4():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    total_points = 0

    for line in lines:
        winning_nums = list(map(int, ((line.split(' | ')[0]).split(": ")[1].strip().replace('  ', ' ')).split(' ')))
        print('wn')
        print(winning_nums)

        elf_nums = list(map(int, ((line.split(' | ')[1]).strip().replace('  ', ' ')).split(' ')))
        print('en')
        print(elf_nums)

        ticket_hits = len([n for n in elf_nums if n in winning_nums])
        # print(ticket_hits)

        if ticket_hits > 0:
            total_points += pow(2, ticket_hits - 1)

    print(f'Total Points: {total_points}\n############################\n')


day_4()

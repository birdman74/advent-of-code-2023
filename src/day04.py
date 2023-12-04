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
    card_copies = {}

    for i in range(len(lines)):
        line = lines[i]

        card_num = i + 1

        winning_nums = list(map(int, ((line.split(' | ')[0]).split(": ")[1].strip().replace('  ', ' ')).split(' ')))
        # print(winning_nums)

        elf_nums = list(map(int, ((line.split(' | ')[1]).strip().replace('  ', ' ')).split(' ')))
        # print(elf_nums)

        ticket_hits = len([n for n in elf_nums if n in winning_nums])
        # print(ticket_hits)

        if ticket_hits > 0:
            total_points += pow(2, ticket_hits - 1)
            copies_of_current_card = 1
            if card_num in card_copies.keys():
                copies_of_current_card += card_copies[card_num]

            for j in range(ticket_hits):
                card_copy_num = card_num + j + 1
                if card_copy_num not in card_copies.keys():
                    card_copies[card_copy_num] = copies_of_current_card
                else:
                    card_copies[card_copy_num] += copies_of_current_card

    total_cards = len(lines) + sum(card_copies.values())

    print(f'Total Points: {total_points}\n############################\n')
    print(f'Total Cards: {total_cards}\n############################\n')


day_4()

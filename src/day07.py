import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day07.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

CARD_STRENGTH = '23456789TJQKA'
FIVE = '5OAK'
FOUR = '4OAK'
FULL_HOUSE = 'FH'
THREE = '3OAK'
TWO_PAIR = '2P'
PAIR = 'P'
HIGH_CARD = 'HC'
TYPE_STRENGTH = [HIGH_CARD, PAIR, TWO_PAIR, THREE, FULL_HOUSE, FOUR, FIVE]


def day_07():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    hands = []

    for line in lines:
        parts = line.split(' ')
        hand = parts[0]
        bid = int(parts[1])
        hands.append((hand, bid, hand_type(hand)))

    ordered_hands = []

    while len(hands) > 1:
        high_hand_index = 0
        for i in range(1, len(hands)):
            if first_hand_higher(hands[i], hands[high_hand_index]):
                high_hand_index = i

        ordered_hands.append(hands[high_hand_index])
        hands.remove(hands[high_hand_index])

    ordered_hands.append(hands[0])

    total_winnings = 0
    for i in range(len(ordered_hands)):
        hand = ordered_hands[i]
        total_winnings += (hand[1] * (len(ordered_hands) - i))

    print(f'Total Winnings: {total_winnings}\n############################\n')


def first_hand_higher(hand_one, hand_two):
    type_strength_1 = TYPE_STRENGTH.index(hand_one[2])
    type_strength_2 = TYPE_STRENGTH.index(hand_two[2])
    if type_strength_1 > type_strength_2:
        return True
    elif type_strength_1 < type_strength_2:
        return False
    else:
        return first_hand_higher_within_type(hand_one, hand_two)


def first_hand_higher_within_type(hand_one, hand_two):
    for i in range(len(hand_one[0])):
        card_one_strength = CARD_STRENGTH.index(hand_one[0][i])
        card_two_strength = CARD_STRENGTH.index(hand_two[0][i])
        if card_one_strength > card_two_strength:
            return True
        elif card_one_strength < card_two_strength:
            return False

    return False


def hand_type(cards):
    ranks = {}
    for card in cards:
        if card in ranks.keys():
            ranks[card] += 1
        else:
            ranks[card] = 1

    if len(ranks) == 5:
        return HIGH_CARD
    elif len(ranks) == 1:
        return FIVE
    elif len(ranks) == 4:
        return PAIR
    elif len(ranks) == 2:
        if 4 in ranks.values():
            return FOUR
        else:
            return FULL_HOUSE
    else:
        if 3 in ranks.values():
            return THREE
        else:
            return TWO_PAIR


day_07()

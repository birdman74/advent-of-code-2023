import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day25.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


def day_25():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    components = {}
    pairs = []

    for line in lines:
        pieces = line.split(': ')
        name = pieces[0]
        connections = set(pieces[1].split())

        for connection in connections:
            add_to_dict(components, name, connection)
            add_to_dict(components, connection, name)
            pairs.append((name, connection))

    for pair in pairs:
        reverse = (pair[1], pair[0])
        if reverse in pairs:
            pairs.remove(reverse)

    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            for k in range(j + 1, len(pairs)):
                severed = [pairs[i], pairs[j], pairs[k]]
                print(f'Testing severed: {severed}')

                product = calc_product_if_severed_correct(components, severed)
                if product > 0:
                    print(f'Product of group sizes: {product}\n############################\n')
                    return


def calc_product_if_severed_correct(comp_dict, severed):
    group_sizes = []

    unvisited = list(comp_dict.keys())
    while len(unvisited) > 0:
        group_sizes.append(components_connected(comp_dict, unvisited, severed))

    if len(group_sizes) == 2:
        return group_sizes[0] * group_sizes[1]
    else:
        return 0


def components_connected(comp_dict, unvisited, severed):
    root = unvisited[0]
    visited = [root]
    next_visits = [root]
    total = 1

    while len(next_visits) > 0:
        new_visits = []
        for c in next_visits:
            unvisited.remove(c)

            for c2 in comp_dict[c]:
                conn = (c, c2)
                rev_conn = (c2, c)
                if c2 not in visited and conn not in severed and rev_conn not in severed:
                    visited.append(c2)
                    new_visits.append(c2)
                    total += 1
        next_visits = new_visits

    return total


def add_to_dict(comp_dict, name, connection):
    if name not in comp_dict.keys():
        comp_dict[name] = {connection}
    else:
        comp_dict[name].add(connection)


day_25()

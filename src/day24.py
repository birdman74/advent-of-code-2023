import os
import numpy as np

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day24.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

TIME_SAMPLE = 5


def day_24():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    stone_data = data_file.read().split('\n')

    stones = []
    velocities = []
    ms = []
    bs = []

    for data in stone_data:
        pieces = data.split(' @ ')
        stone = tuple(list(map(int, pieces[0].strip().split(', '))))
        velocity = tuple(list(map(int, pieces[1].strip().split(', '))))
        b = stone[1] - ((velocity[1] / velocity[0]) * stone[0])
        stones.append(stone)
        velocities.append(velocity)
        ms.append(velocity[1] / velocity[0])
        bs.append(b)

    x = 0
    y = 0
    z = 0

    for a in range(51, len(stones)):
        print(f'a = {a}')
        for b in range(len(stones)):
            print('#', end='')
            if a == b:
                continue
            for c in range(len(stones)):
                if a == c or b == c:
                    continue

                stone_indices = [a, b, c]
                # print(f'Stone Indices: {stone_indices}')
                stone_sample = [stones[i] for i in stone_indices]
                velocity_sample = [velocities[i] for i in stone_indices]
                positions_t = []

                for t in range(TIME_SAMPLE):
                    positions = []
                    positions_t.append(positions)
                    for i in range(len(stone_sample)):
                        positions.append(np.add(stone_sample[i], np.multiply(velocity_sample[i], t)))

                    # print(f'Time: {t}, Positions: {positions}')

                for i in range(len(stone_sample)):
                    # print(f'Base Rock: {stone_sample[i]}, velocity: {velocity_sample[i]}\n')
                    other_indices = list(range(len(stone_sample)))
                    other_indices.remove(i)
                    other_samples = []
                    for base_rock_t in range(len(positions_t)):
                        other_sample_at_t = []
                        # print(f'Base rock time: {base_rock_t}')
                        base_rock_position = positions_t[base_rock_t][i]
                        for t in range(len(positions_t)):
                            # print(f'Time: {t}')
                            sample = list(np.subtract(positions_t[t], base_rock_position))
                            sample = [sample[i1] for i1 in other_indices]
                            other_sample_at_t.append(sample)
                            # print(sample)

                        other_samples.append(other_sample_at_t)
                        # print()

                    for base_rock_t in range(1, len(other_samples)):
                        samples = other_samples[base_rock_t]
                        for rock1_t_index in range(1, len(samples)):
                            for rock2_t_index in range(1, len(samples)):
                                if rock1_t_index == rock2_t_index or base_rock_t in [rock1_t_index, rock2_t_index]:
                                    continue

                                if np.array_equal(np.divide(samples[rock1_t_index][0], base_rock_t - rock1_t_index),
                                                  np.divide(samples[rock2_t_index][1], base_rock_t - rock2_t_index)):
                                    print(f'Found a match at base rock t = {base_rock_t}.\n Rock 1 time: {rock1_t_index} Rock 2 time: {rock2_t_index}')
        print()

    print(f'Sum of initial magical rock coordinates: {x + y + z}\n############################\n')


day_24()

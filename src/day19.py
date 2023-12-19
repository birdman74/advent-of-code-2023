import copy
import os
from enum import Enum
from functools import reduce

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day19.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

REJECTED = 'R'
ACCEPTED = 'A'
INITIAL_WORKFLOW = 'in'
MIN_RATING = 1
MAX_RATING = 4000


class Comparison(Enum):
    GT = '>'
    LT = '<'


def day_19():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    possible_ratings_combos = 0

    workflows = {}
    for line in lines:
        if not line:
            break

        p1 = line.split('{')
        name = p1[0]
        p2 = p1[1]
        rules = p2.split(',')
        wf = Workflow(rules[-1][0:-1])
        for i in range(len(rules) - 1):
            rule = rules[i]

            p3 = rule.split(':')
            trait = p3[0][0]
            comparison = Comparison(p3[0][1])
            value = int(p3[0][2:])
            destination = p3[1]
            wf.rules.append(Rule(trait, comparison, value, destination))
        workflows[name] = wf

    accepted_paths = []
    path_restrictions = []
    workflows[INITIAL_WORKFLOW].calc_acceptable_trait_ranges(workflows,
                                                             accepted_paths,
                                                             path_restrictions)

    possible_ratings_combos = process_accepted_paths(accepted_paths)

    print(f'Total possible ratings combos: {possible_ratings_combos}\n############################\n')


def process_accepted_paths(accepted_paths):
    total_combos = 0

    for accepted_path in accepted_paths:
        init_acceptable_ranges = {'x': range(MIN_RATING, MAX_RATING + 1),
                                  'm': range(MIN_RATING, MAX_RATING + 1),
                                  'a': range(MIN_RATING, MAX_RATING + 1),
                                  's': range(MIN_RATING, MAX_RATING + 1)}
        for condition in accepted_path:
            trait = condition[0]
            t_range = condition[1]
            a_range = init_acceptable_ranges[trait]
            init_acceptable_ranges[trait] = range(max(a_range.start, t_range.start), min(a_range.stop, t_range.stop))

        total_combos += reduce(lambda x, y: x*y, [r.stop - r.start for r in init_acceptable_ranges.values()])
    return total_combos


def process_part(workflows, raw_data):
    traits = {}
    raw_traits = raw_data[1:-1].split(',')
    for t in raw_traits:
        p = t.split('=')
        traits[p[0]] = int(p[1])

    return workflows[INITIAL_WORKFLOW].process(traits, workflows)


class Workflow:
    def __init__(self, default):
        self.rules = []
        self.default = default

    def calc_acceptable_trait_ranges(self, workflows, accepted_paths, path_restrictions):
        chain_restrictions = copy.deepcopy(path_restrictions)
        for rule in self.rules:
            if rule.destination == ACCEPTED:
                accepted_paths.append(chain_restrictions + [rule.restriction])
            elif rule.destination != REJECTED:
                workflows[rule.destination].calc_acceptable_trait_ranges(workflows,
                                                                         accepted_paths,
                                                                         chain_restrictions + [rule.restriction])

            chain_restrictions.append(rule.negative_restriction)

        if self.default == ACCEPTED:
            accepted_paths.append(chain_restrictions)
        elif self.default != REJECTED:
            workflows[self.default].calc_acceptable_trait_ranges(workflows,
                                                                 accepted_paths,
                                                                 chain_restrictions)

    def process(self, traits, workflows):
        for rule in self.rules:
            if rule.satisfied(traits):
                if rule.destination == ACCEPTED:
                    return sum([v for v in traits.values()])
                elif rule.destination == REJECTED:
                    return 0
                else:
                    return workflows[rule.destination].process(traits, workflows)

        if self.default == ACCEPTED:
            return sum([v for v in traits.values()])
        elif self.default == REJECTED:
            return 0
        else:
            return workflows[self.default].process(traits, workflows)


class Rule:
    def __init__(self, trait, comparison, value, destination):
        self.trait = trait
        self.comparison = comparison
        self.value = value
        self.destination = destination
        self.restriction = {}
        self.negative_restriction = {}
        self.set_restrictions()

    def __repr__(self):
        return f'{self.trait} {self.comparison.value} {self.value} => {self.destination}'

    def set_restrictions(self):
        match self.comparison:
            case Comparison.GT:
                self.negative_restriction = [self.trait, range(MIN_RATING, self.value + 1)]
                self.restriction = [self.trait, range(self.value + 1, MAX_RATING + 1)]
            case _:
                self.restriction = [self.trait, range(MIN_RATING, self.value)]
                self.negative_restriction = [self.trait, range(self.value, MAX_RATING + 1)]

    def satisfied(self, traits):
        val = traits[self.trait]
        match self.comparison:
            case Comparison.GT:
                return val > self.value
            case _:
                return val < self.value


day_19()

import os
from enum import Enum

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day19.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

REJECTED = 'R'
ACCEPTED = 'A'
INITIAL_WORKFLOW = 'in'


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

    accepted_parts_ratings_sum = 0

    workflows = {}
    run_workflow = False
    for line in lines:
        if not line:
            run_workflow = True
            continue

        if not run_workflow:
            p1 = line.split('{')
            name = p1[0]
            p2 = p1[1]
            instructions = p2.split(',')
            wf = Workflow(instructions[-1][0:-1])
            for i in range(len(instructions) - 1):
                instruction = instructions[i]

                p3 = instruction.split(':')
                trait = p3[0][0]
                comparison = Comparison(p3[0][1])
                value = int(p3[0][2:])
                destination = p3[1]
                wf.rules.append(Evaluation(trait, comparison, value, destination))
            workflows[name] = wf
        else:
            accepted_parts_ratings_sum += process_part(workflows, line)

    print(f'Accepted parts rating sum: {accepted_parts_ratings_sum}\n############################\n')


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


class Evaluation:
    def __init__(self, trait, comparison, value, destination):
        self.trait = trait
        self.comparison = comparison
        self.value = value
        self.destination = destination

    def satisfied(self, traits):
        val = traits[self.trait]
        match self.comparison:
            case Comparison.GT:
                return val > self.value
            case _:
                return val < self.value


day_19()

import collections
import itertools
import re

from utils import parse_input


def part_1(steps):
    return map_steps(steps)


def part_2(steps):
    return time_steps(steps, 5, 60)


def parse_steps(steps):
    return [re.match(r'Step (\w) must be finished before step (\w) can begin.', l).groups() for l in steps]


def map_steps(steps):
    all_steps = set(itertools.chain.from_iterable(steps))
    step_deps = collections.defaultdict(set)
    for step in steps:
        step_deps[step[1]].add(step[0])
    done_steps = set()
    todo_steps = all_steps
    completed_order = []

    while todo_steps:
        for step in sorted(todo_steps):
            if all(dep in done_steps for dep in step_deps[step]):
                done_steps.add(step)
                todo_steps.remove(step)
                completed_order.append(step)
                break
    return ''.join(completed_order)


def time_steps(steps, num_workers, extra_time):
    all_steps = set(itertools.chain.from_iterable(steps))
    step_deps = collections.defaultdict(set)
    for step in steps:
        step_deps[step[1]].add(step[0])
    done_steps = set()
    todo_steps = all_steps
    completed_order = []
    complete_steps = set()
    progress_steps = set()

    workers = [{'task': None, 'time': 0} for x in range(num_workers)]

    t = 0

    while todo_steps | progress_steps:
        if complete_steps:
            done_steps.update(complete_steps)
            complete_steps = set()
        # print(t)
        for i, worker in enumerate(workers):
            # print('Worker', i)
            if worker['task'] is None:
                for step in sorted(todo_steps):
                    if all(dep in done_steps for dep in step_deps[step]):
                        # print('Task', step)
                        todo_steps.remove(step)
                        progress_steps.add(step)
                        worker['task'] = step
                        worker['time'] = 1
                        break
            else:
                worker['time'] += 1
                if worker['time'] >= ord(worker['task']) - 64 + extra_time:
                    complete_steps.add(worker['task'])
                    progress_steps.remove(worker['task'])
                    worker['task'] = None

        print(t, [(i, w['task']) for i, w in enumerate(workers)], ''.join(complete_steps | done_steps))
        t += 1

    return t


TEST_STEPS = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''


def test_parse_steps():
    assert parse_steps(TEST_STEPS.splitlines()) == [
        ('C', 'A'), ('C', 'F'), ('A', 'B'), ('A', 'D'), ('B', 'E'), ('D', 'E'), ('F', 'E')
    ]


def test_map_steps():
    assert map_steps(parse_steps(TEST_STEPS.splitlines())) == 'CABDFE'


def test_time_steps():
    assert time_steps(parse_steps(TEST_STEPS.splitlines()), 2, 0) == 15


if __name__ == '__main__':
    steps = parse_input('input_7.txt')
    steps = parse_steps(steps)
    print(part_1(steps))
    print(part_2(steps))

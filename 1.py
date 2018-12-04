import itertools

from utils import parse_input


def part_1():
    changes = parse_input(1)
    return sum_changes(changes)


def part_2():
    changes = parse_input(1)
    return first_duplicate_frequency(changes)


def sum_changes(changes):
    return sum(int(charge) for charge in changes)


def first_duplicate_frequency(changes):
    i = 0
    seen = {i}
    for change in itertools.chain.from_iterable(itertools.repeat(changes)):
        i += int(change)
        if i in seen:
            return i
        seen.add(i)


def test_sum_changes():
    assert sum_changes(['+1', '-2', '+3', '+1']) == 3
    assert sum_changes(['+1', '+1', '+1']) == 3
    assert sum_changes(['+1', '+1', '-2']) == 0
    assert sum_changes(['-1', '-2', '-3']) == -6


def test_first_duplicate_frequency():
    assert first_duplicate_frequency(['+1', '-2', '+3', '+1']) == 2
    assert first_duplicate_frequency(['+1', '-1']) == 0
    assert first_duplicate_frequency(['+3', '+3', '+4', '-2', '-4']) == 10
    assert first_duplicate_frequency(['-6', '+3', '+8', '+5', '-6']) == 5
    assert first_duplicate_frequency(['+7', '+7', '-2', '-7', '-4']) == 14


if __name__ == '__main__':
    print(part_1())
    print(part_2())

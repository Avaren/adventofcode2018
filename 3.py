import collections
import itertools
import re

from utils import parse_input


def part_1(claims):
    claims = (to_claim(claim) for claim in claims)
    total_overlap = set()
    for claim1, claim2 in itertools.combinations(claims, 2):
        total_overlap.update(claim1.overlap(claim2))
    return len(total_overlap)


def part_2(claims):
    claims = [to_claim(claim) for claim in claims]
    for claim in claims:
        overlap = False
        for c1, c2 in itertools.product([claim], claims):
            if c1.id == c2.id: continue
            if c1.overlap(c2):
                overlap = True
                break
        if not overlap:
            return claim


Claim = collections.namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])


class Claim(Claim):

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    def overlap(self, claim):
        if (self.right <= claim.left) | (claim.right <= self.left):
            return []

        if (self.bottom <= claim.top) | (claim.bottom <= self.top):
            return []

        left = max(self.left, claim.left)
        right = min(self.right, claim.right)
        top = max(self.top, claim.top)
        bottom = min(self.bottom, claim.bottom)
        return [(i, j) for i in range(left, right) for j in range(top, bottom)]


def to_claim(line):
    matches = re.match(r'\#(\d+) \@ (\d+),(\d+): (\d+)x(\d+)', line)
    return Claim(*[int(g) for g in matches.groups()])


def test_to_claim():
    assert to_claim('#1 @ 1,3: 4x4') == Claim(1, 1, 3, 4, 4)
    assert to_claim('#2 @ 3,1: 4x4') == Claim(2, 3, 1, 4, 4)
    assert to_claim('#3 @ 5,5: 2x2') == Claim(3, 5, 5, 2, 2)


def test_overlap():
    one = Claim(1, 1, 3, 4, 4)
    two = Claim(2, 3, 1, 4, 4)
    three = Claim(3, 5, 5, 2, 2)

    assert three.overlap(one) == []
    assert three.overlap(two) == []
    assert one.overlap(two) == [(3, 3), (3, 4), (4, 3), (4, 4)]


if __name__ == '__main__':
    inputs = parse_input('input_3.txt')
    print(part_1(inputs))
    print(part_2(inputs))

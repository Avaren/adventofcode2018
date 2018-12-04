import collections
import itertools

from utils import parse_input


def part_1(packages):
    return calculate_checksum(packages)


def part_2(packages):
    return common_code(packages)


def calculate_checksum(packages):
    twos = threes = 0
    for package in packages:
        has_two, has_three = has_multiple(package)
        twos += has_two
        threes += has_three
    return twos * threes


def has_multiple(package):
    has_two = has_three = False
    count = collections.Counter(package)
    for v in count.values():
        if v == 2:
            has_two = True
        elif v == 3:
            has_three = True
    return has_two, has_three


def common_code(packages):
    for pkg1, pkg2 in itertools.combinations(packages, 2):
        if almost_same(pkg1, pkg2):
            return ''.join(i for i, j in zip(pkg1, pkg2) if i == j)


def almost_same(pkg1, pkg2):
    diffs = 0
    for i, j in zip(pkg1, pkg2):
        if i != j:
            diffs += 1
        if diffs > 1:
            return False

    return True


def test_has_multiple():
    assert has_multiple('abcdef') == (False, False)
    assert has_multiple('bababc') == (True, True)
    assert has_multiple('abbcde') == (True, False)
    assert has_multiple('abcccd') == (False, True)
    assert has_multiple('aabcdd') == (True, False)
    assert has_multiple('abcdee') == (True, False)
    assert has_multiple('ababab') == (False, True)


def test_calculate_checksum():
    packages = [
        'abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee', 'ababab',
    ]
    assert calculate_checksum(packages) == 12


def test_almost_same():
    assert almost_same('abcde', 'fghij') == False
    assert almost_same('abcde', 'klmno') == False
    assert almost_same('abcde', 'pqrst') == False
    assert almost_same('abcde', 'fguij') == False
    assert almost_same('abcde', 'axcye') == False
    assert almost_same('abcde', 'wvxyz') == False
    assert almost_same('fghij', 'klmno') == False
    assert almost_same('fghij', 'pqrst') == False
    assert almost_same('fghij', 'fguij') == True
    assert almost_same('fghij', 'axcye') == False
    assert almost_same('fghij', 'wvxyz') == False
    assert almost_same('klmno', 'pqrst') == False
    assert almost_same('klmno', 'fguij') == False
    assert almost_same('klmno', 'axcye') == False
    assert almost_same('klmno', 'wvxyz') == False
    assert almost_same('pqrst', 'fguij') == False
    assert almost_same('pqrst', 'axcye') == False
    assert almost_same('pqrst', 'wvxyz') == False
    assert almost_same('fguij', 'axcye') == False
    assert almost_same('fguij', 'wvxyz') == False
    assert almost_same('axcye', 'wvxyz') == False


def test_common_code():
    assert common_code(['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']) == 'fgij'


if __name__ == '__main__':
    inputs = parse_input('input_2.txt')
    print(part_1(inputs))
    print(part_2(inputs))

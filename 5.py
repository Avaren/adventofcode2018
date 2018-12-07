def part_1(polymer):
    return len(react_polymer(polymer))


def part_2(polymer):
    units = set(polymer.lower())
    return min(
        len(react_polymer(remove_unit(polymer, u))) for u in units
    )


def react_polymer(polymer):
    reaction = True
    start = 0
    while reaction:
        reaction = False
        if polymer:
            for i in range(start, len(polymer) - 1):
                if polymer[i] == polymer[i + 1]:
                    continue
                if polymer[i] == polymer[i + 1].upper() or polymer[i] == polymer[i + 1].lower():
                    polymer = polymer[:i] + polymer[i + 2:]
                    reaction = True
                    start = max(0, i - 1)  # optimisation, only need to reprocess part of the polymer
                    break
    return polymer


def remove_unit(polymer, unit):
    unit1, unit2 = unit.lower(), unit.upper()
    return polymer.replace(unit1, '').replace(unit2, '')


def test_react_polymer():
    assert react_polymer('aA') == ''
    assert react_polymer('abBA') == ''
    assert react_polymer('abAB') == 'abAB'
    assert react_polymer('aabAAB') == 'aabAAB'
    assert react_polymer('dabAcCaCBAcCcaDA') == 'dabCBAcaDA'


def test_remove_unit():
    assert remove_unit('dabAcCaCBAcCcaDA', 'a') == 'dbcCCBcCcD'
    assert react_polymer(remove_unit('dabAcCaCBAcCcaDA', 'a')) == 'dbCBcD'

    assert remove_unit('dabAcCaCBAcCcaDA', 'b') == 'daAcCaCAcCcaDA'
    assert react_polymer(remove_unit('dabAcCaCBAcCcaDA', 'b')) == 'daCAcaDA'

    assert remove_unit('dabAcCaCBAcCcaDA', 'c') == 'dabAaBAaDA'
    assert react_polymer(remove_unit('dabAcCaCBAcCcaDA', 'c')) == 'daDA'

    assert remove_unit('dabAcCaCBAcCcaDA', 'd') == 'abAcCaCBAcCcaA'
    assert react_polymer(remove_unit('dabAcCaCBAcCcaDA', 'd')) == 'abCBAc'


if __name__ == '__main__':
    with open('input_5.txt') as f:
        polymer = f.read()
    print(part_1(polymer))
    print(part_2(polymer))

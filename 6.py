import collections
import itertools
import operator
from string import ascii_lowercase, ascii_uppercase

from utils import parse_input


def part_1(points):
    bounds = map_bounds(points)
    p = closest_points(bounds, points)
    areas = point_areas(p)
    return biggest_area(bounds, areas, points, p)


def part_2(points):
    bounds = map_bounds(points)
    pd = distance_to_points(bounds, points)
    return len(closest_region(pd, 10000))


def filter_infinite_areas(points, bounds, point_map):
    on_edge = set()

    for i in range(bounds[0], bounds[2] + 1):
        for j in [bounds[1], bounds[3]]:
            if len(point_map[(i, j)]) > 1:
                continue
            on_edge.add(point_map[(i, j)][0])

    for j in range(bounds[1], bounds[3] + 1):
        for i in [bounds[0], bounds[2]]:
            if len(point_map[(i, j)]) > 1:
                continue
            on_edge.add(point_map[(i, j)][0])

    return set(points) - on_edge


def map_bounds(points):
    return (
        min(points, key=operator.itemgetter(0))[0],
        min(points, key=operator.itemgetter(1))[1],
        max(points, key=operator.itemgetter(0))[0],
        max(points, key=operator.itemgetter(1))[1],
    )


def closest_points(bounds, points):
    closest_point_map = collections.defaultdict(list)
    for i in range(bounds[0], bounds[2] + 1):
        for j in range(bounds[1], bounds[3] + 1):
            point_map = {}
            for point in points:
                point_map[point] = dist(point, (i, j))
            smallest = min(point_map.values())
            closest_point_map[(i, j)] = [point for point, d in point_map.items() if d == smallest]
    return closest_point_map


def point_areas(closest_point_map):
    areas = collections.defaultdict(list)
    for point, closest in closest_point_map.items():
        if len(closest) > 1:
            continue
        areas[closest[0]].append(point)
    return areas


def biggest_area(bounds, areas, points, point_map):
    valid_areas = filter_infinite_areas(points, bounds, point_map)
    areas = {point: points for point, points in areas.items() if point in valid_areas}
    return len(max(areas.items(), key=lambda x: len(x[1]))[1])


def dist(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])


TEST_POINTS = [
    (1, 1),
    (1, 6),
    (8, 3),
    (3, 4),
    (5, 5),
    (8, 9),
]


def draw_map(points, bounds, closest_points):
    m = []
    point_key = dict(zip(points, itertools.chain.from_iterable(itertools.repeat(ascii_lowercase))))
    for j in range(bounds[1], bounds[3] + 1):
        r = []
        for i in range(bounds[0], bounds[2] + 1):
            if len(closest_points[(i, j)]) > 1:
                char = '.'
            elif (i, j) in point_key:
                char = point_key[(i, j)].upper()
            else:
                char = point_key[closest_points[(i, j)][0]]
            r.append(char)
        m.append(''.join(r))
    return '\n'.join(m)


def draw_region_map(points, bounds, regions):
    m = []
    point_key = dict(zip(points, itertools.chain.from_iterable(itertools.repeat(ascii_uppercase))))
    for j in range(bounds[1], bounds[3] + 1):
        r = []
        for i in range(bounds[0], bounds[2] + 1):
            if (i, j) in point_key:
                char = point_key[(i, j)].upper()
            elif (i, j) in regions:
                char = '#'
            else:
                char = '.'
            r.append(char)
        m.append(''.join(r))
    return '\n'.join(m)


def test_map_bounds():
    assert map_bounds(TEST_POINTS) == (1, 1, 8, 9)


def test_filter_infinite_points():
    bounds = map_bounds(TEST_POINTS)
    p = closest_points(bounds, TEST_POINTS)
    assert filter_infinite_areas(TEST_POINTS, bounds, p) == {(3, 4), (5, 5)}


def test_point_areas():
    bounds = map_bounds(TEST_POINTS)
    m = closest_points(bounds, TEST_POINTS)
    areas = point_areas(m)
    assert len(areas[(3, 4)]) == 9
    assert len(areas[(5, 5)]) == 17


TEST_MAP = '''Aaaa.ccc
aaddeccc
adddeccC
.dDdeecc
b.deEeec
Bb.eeee.
bb.eeeff
bb.eefff
bb.ffffF'''


def test_draw_map():
    bounds = map_bounds(TEST_POINTS)
    p = closest_points(bounds, TEST_POINTS)
    m = draw_map(TEST_POINTS, bounds, p)
    assert m == TEST_MAP


def test_biggest_area():
    bounds = map_bounds(TEST_POINTS)
    p = closest_points(bounds, TEST_POINTS)
    areas = point_areas(p)
    assert biggest_area(bounds, areas, TEST_POINTS, p) == 17


def distance_to_points(bounds, points):
    point_dist = {}
    for j in range(bounds[1], bounds[3] + 1):
        for i in range(bounds[0], bounds[2] + 1):
            point_dist[(i, j)] = sum(
                dist((i, j), p) for p in points
            )
    return point_dist


def closest_region(point_dist, max_dist):
    return {p for p, d in point_dist.items() if d < max_dist}


def test_distance_to_points():
    bounds = map_bounds(TEST_POINTS)
    assert distance_to_points(bounds, TEST_POINTS)[(4, 3)] == 30


def test_closest_region():
    bounds = map_bounds(TEST_POINTS)
    pd = distance_to_points(bounds, TEST_POINTS)
    assert len(closest_region(pd, 32)) == 16


TEST_REGION_MAP = '''A.......
........
..###..C
.#D###..
.###E#..
B.###...
........
........
.......F'''


def test_draw_region_map():
    bounds = map_bounds(TEST_POINTS)
    pd = distance_to_points(bounds, TEST_POINTS)
    r = closest_region(pd, 32)
    assert draw_region_map(TEST_POINTS, bounds, r) == TEST_REGION_MAP


if __name__ == '__main__':
    points = parse_input('input_6.txt')
    points = [tuple(int(i) for i in r.split(',')) for r in points]
    print(part_1(points))
    print(part_2(points))

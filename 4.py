import collections
import datetime
import operator
import re

from utils import parse_input


def part_1(schedule):
    schedule = parse_schedule(schedule)
    guards = determine_sleep(schedule)
    sleepiest_guard = sorted(guards.values(), key=operator.attrgetter('total_sleep'), reverse=True)[0]
    print(sleepiest_guard.id, sleepiest_guard.most_asleep.most_common(1))
    return sleepiest_guard.id * sleepiest_guard.most_asleep.most_common(1)[0][0].minute


def part_2(schedule):
    schedule = parse_schedule(schedule)
    guards = determine_sleep(schedule)

    key = lambda g: g.most_asleep.most_common(1)[0][1]

    most_consistent_guard = sorted(guards.values(), key=key, reverse=True)[0]
    print(most_consistent_guard.id, most_consistent_guard.most_asleep.most_common(1))
    return most_consistent_guard.id * most_consistent_guard.most_asleep.most_common(1)[0][0].minute


Guard = collections.namedtuple('Guard', ['id', 'minutes_asleep'])


class Guard(Guard):

    @property
    def total_sleep(self):
        return sum(True for i in self.minutes_asleep)

    @property
    def most_asleep(self):
        return collections.Counter(self.minutes_asleep)


def parse_schedule(schedule):
    results = []
    for line in schedule:
        match = re.match(r'\[([^]]+)\] (.*)', line)
        time = datetime.datetime.strptime(match.group(1), '%Y-%m-%d %H:%M')
        results.append((time, match.group(2)))

    return sorted(results)


def determine_sleep(schedule):
    guards = collections.defaultdict(list)
    guard = sleep_start = None
    sleep_mins = []
    for event in schedule:
        if event[1].startswith('Guard'):
            if sleep_mins:
                guards[guard].extend(sleep_mins)
            guard = int(re.match(r'Guard \#(\d+)', event[1]).group(1))
            sleep_start = None
            sleep_mins = []
        else:
            if event[1] == 'falls asleep':
                sleep_start = event[0]
            elif event[1] == 'wakes up':
                sleep_end = event[0]
                while sleep_start < sleep_end:
                    sleep_mins.append(sleep_start.time())
                    sleep_start += datetime.timedelta(minutes=1)
            else:
                raise RuntimeError(event[0], event[1])
    if sleep_mins:
        guards[guard].extend(sleep_mins)
    return {g.id: g for g in (Guard(id, mins) for id, mins in guards.items())}


test_schedule = '''[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up'''.splitlines()

test_result_schedule = [
    (datetime.datetime(1518, 11, 1, 0, 0), 'Guard #10 begins shift'),
    (datetime.datetime(1518, 11, 1, 0, 5), 'falls asleep'),
    (datetime.datetime(1518, 11, 1, 0, 25), 'wakes up'),
    (datetime.datetime(1518, 11, 1, 0, 30), 'falls asleep'),
    (datetime.datetime(1518, 11, 1, 0, 55), 'wakes up'),
    (datetime.datetime(1518, 11, 1, 23, 58), 'Guard #99 begins shift'),
    (datetime.datetime(1518, 11, 2, 0, 40), 'falls asleep'),
    (datetime.datetime(1518, 11, 2, 0, 50), 'wakes up'),
    (datetime.datetime(1518, 11, 3, 0, 5), 'Guard #10 begins shift'),
    (datetime.datetime(1518, 11, 3, 0, 24), 'falls asleep'),
    (datetime.datetime(1518, 11, 3, 0, 29), 'wakes up'),
    (datetime.datetime(1518, 11, 4, 0, 2), 'Guard #99 begins shift'),
    (datetime.datetime(1518, 11, 4, 0, 36), 'falls asleep'),
    (datetime.datetime(1518, 11, 4, 0, 46), 'wakes up'),
    (datetime.datetime(1518, 11, 5, 0, 3), 'Guard #99 begins shift'),
    (datetime.datetime(1518, 11, 5, 0, 45), 'falls asleep'),
    (datetime.datetime(1518, 11, 5, 0, 55), 'wakes up')
]


def test_parse_schedule():
    assert parse_schedule(test_schedule) == test_result_schedule


def test_determine_sleep():
    results = determine_sleep(test_result_schedule)
    assert results[10].total_sleep == 50
    assert results[10].most_asleep.most_common(1) == [(datetime.time(0, 24), 2)]
    assert results[99].total_sleep == 30
    assert results[99].most_asleep.most_common(1) == [(datetime.time(0, 45), 3)]


if __name__ == '__main__':
    inputs = parse_input('input_4.txt')
    print(part_1(inputs))
    print(part_2(inputs))

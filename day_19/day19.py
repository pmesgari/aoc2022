import sys
import re
from collections import namedtuple


BluePrint = namedtuple(
    'Blueprint', 'OreRobot ClayRobot ObsidianRobot GeodeRobot')

OreRobot = namedtuple('OreRobot', 'ore_cost')
ClayRobot = namedtuple('ClayRobot', 'ore_cost')
ObsidianRobot = namedtuple('ObsidianRobot', 'ore_cost clay_cost')
GeodeRobot = namedtuple('GeodeRobot', 'ore_cost obsidian_cost')

Robots = namedtuple('Robots', 'ore clay obsidian geode')
Materials = namedtuple('Materials', 'ore clay obsidian geode')

State = namedtuple('State', 'time robots materials skipped')

RobotIDs = {
    'ORE': 0,
    'CLAY': 1,
    'OBS': 2,
    'GEO': 3
}


def parse_input(sample):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    exp = re.compile(r'\d+')
    costs = []
    with open(filename) as f:
        for line in f:
            costs.append(tuple(map(int, exp.findall(line))))

    blueprints = []
    for cost in costs:
        blueprints.append(
            BluePrint(
                OreRobot(cost[1]),
                ClayRobot(cost[2]),
                ObsidianRobot(cost[3], cost[4]),
                GeodeRobot(cost[5], cost[6])
            )
        )
    return blueprints


def optimistic_best(start, robots, t):
    return start + robots * (t + 1) + t * (t + 1) // 2


def search(bp: BluePrint, time, debug=False):
    max_ore_needed = max(bp, key=lambda x: x[0])[0]
    max_clay_needed = bp.ObsidianRobot.clay_cost
    max_obsidian_needed = bp.GeodeRobot.obsidian_cost
    time = 24
    best = 0
    visited = set()
    # print(max_ore_needed, max_clay_needed, max_obsidian_needed)
    Q = [State(time, Robots(1, 0, 0, 0), Materials(0, 0, 0, 0), [])]

    count = 0
    while Q:
        current_state = Q.pop()
        current_time, current_robots, current_materials, skipped = current_state

        if (current_time, current_robots, current_materials) in visited:
            continue

        visited.add((current_time, current_robots, current_materials))
        newore = current_materials.ore + current_robots.ore
        newclay = current_materials.clay + current_robots.clay
        newobsidian = current_materials.obsidian + current_robots.obsidian
        newgeode = current_materials.geode + current_robots.geode
        if count in [4, 5] and debug:
            print(f'state: {(current_time, current_robots, current_materials)}')
            print(f'newore: {newore}, newclay: {newclay}, newobsidian: {newobsidian}, newgeod: {newgeode}')
        count += 1

        current_time -= 1

        if current_time == 0:
            best = max(best, newgeode)
            continue

        if optimistic_best(newgeode, current_robots.geode, current_time) < best:
            continue

        if optimistic_best(newobsidian, current_robots.obsidian, current_time) < bp.GeodeRobot.obsidian_cost:
            best = max(best, newgeode + current_robots.geode * current_time)
            continue

        if optimistic_best(newore, current_robots.ore, current_time) < bp.GeodeRobot.ore_cost:
            best = max(best, newgeode + current_robots.geode * current_time)
            continue

        can_build = []

        # GeodeRobot = namedtuple('GeodeRobot', 'ore_cost obsidian_cost')
        # can we build a GeodeRobot?
        if current_materials.ore >= bp.GeodeRobot.ore_cost:
            if current_materials.obsidian >= bp.GeodeRobot.obsidian_cost:
                if RobotIDs['GEO'] not in skipped:
                    can_build.append(RobotIDs['GEO'])
                    new_robots = Robots(
                        current_robots.ore,
                        current_robots.clay,
                        current_robots.obsidian,
                        current_robots.geode + 1
                    )
                    new_materials = Materials(
                        newore - bp.GeodeRobot.ore_cost,
                        newclay,
                        newobsidian - bp.GeodeRobot.obsidian_cost,
                        newgeode
                    )
                    new_state = (current_time, new_robots, new_materials, [])
                    if current_time == 19 and debug:
                        print(f'geo: {new_state}')
                    Q.append(new_state)

        # ObsidianRobot = namedtuple('ObsidianRobot', 'ore_cost clay_cost')
        # can we build an ObsidianRobot?
        if current_robots.obsidian < max_obsidian_needed:
            if current_materials.clay >= bp.ObsidianRobot.clay_cost:
                if current_materials.ore >= bp.ObsidianRobot.ore_cost:
                    if RobotIDs['OBS'] not in skipped:
                        can_build.append(RobotIDs['OBS'])
                        new_robots = Robots(
                            current_robots.ore,
                            current_robots.clay,
                            current_robots.obsidian + 1,
                            current_robots.geode
                        )
                        new_materials = Materials(
                            newore - bp.ObsidianRobot.ore_cost,
                            newclay - bp.ObsidianRobot.clay_cost,
                            newobsidian,
                            newgeode
                        )
                        new_state = (current_time, new_robots,
                                     new_materials, [])
                        if current_time == 19 and debug:
                            print(f'obs: {new_state}')
                        Q.append(new_state)

        # ClayRobot = namedtuple('ClayRobot', 'ore_cost')
        # can we build a ClayRobot?
        if current_robots.clay < max_clay_needed:
            if current_materials.ore >= bp.ClayRobot.ore_cost:
                if RobotIDs['CLAY'] not in skipped:
                    can_build.append(RobotIDs['CLAY'])
                    new_robots = Robots(
                        current_robots.ore,
                        current_robots.clay + 1,
                        current_robots.obsidian,
                        current_robots.geode
                    )
                    new_materials = Materials(
                        newore - bp.ClayRobot.ore_cost,
                        newclay,
                        newobsidian,
                        newgeode
                    )
                    new_state = (current_time, new_robots, new_materials, [])
                    if current_time == 19 and debug:
                        print(f'clay: {new_state}')
                    Q.append(new_state)

        # OreRobot = namedtuple('OreRobot', 'ore_cost')
        # can we build an OreRobot
        if current_robots.ore < max_ore_needed:
            if current_materials.ore >= bp.OreRobot.ore_cost:
                if RobotIDs['ORE'] not in skipped:
                    can_build.append(RobotIDs['ORE'])
                    new_robots = Robots(
                        current_robots.ore + 1,
                        current_robots.clay,
                        current_robots.obsidian,
                        current_robots.geode
                    )
                    new_materials = Materials(
                        newore - bp.OreRobot.ore_cost,
                        newclay,
                        newobsidian,
                        newgeode
                    )
                    new_state = (current_time, new_robots, new_materials, [])
                    if current_time == 19 and debug:
                        print(f'ore: {new_state}')
                    Q.append(new_state)
        did_not_build_obsidian_robot = current_robots.obsidian and current_materials.obsidian < max_obsidian_needed
        did_not_build_clay_robot = current_robots.clay and current_materials.clay < max_clay_needed
        did_not_produce_ore = current_materials.ore < max_ore_needed
        if did_not_build_obsidian_robot or did_not_build_clay_robot or did_not_produce_ore:
            new_robots = current_robots
            new_materials = Materials(newore, newclay, newobsidian, newgeode)
            new_state = (current_time, new_robots, new_materials, can_build)
            if current_time == 19 and debug:
                print(f'last: {new_state}')
            Q.append(new_state)

    return best


def part1(blueprints):
    scores = []
    for bp in blueprints:
        score = search(bp, 24)
        scores.append(score)

    total = sum([(i + 1) * scores[i] for i in range(len(scores))])
    print(total)


def part2():
    scores = []
    for bp in blueprints[:3]:
        score = search(bp, 32)
        scores.append(score)

    total = scores[0] * scores[1] * scores[2]
    print(total)

if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv
    blueprints = parse_input(sample)
    if p1:
        part1(blueprints)
    elif p2:
        part2(blueprints)

import unittest
import re
import time


class TestToday(unittest.TestCase):
    blueprint_1 = {
        "ore_bot": [("ore", 4)],
        "clay_bot": [("ore", 2)],
        "obs_bot": [("ore", 3), ("clay", 14)],
        "geo_bot": [("ore", 2), ("obs", 7)],
    }
    blueprint_2 = {
        "ore_bot": [("ore", 2)],
        "clay_bot": [("ore", 3)],
        "obs_bot": [("ore", 3), ("clay", 8)],
        "geo_bot": [("ore", 3), ("obs", 12)],
    }
    
    def test_part_1(self):
        test_f = Factario()
        self.assertEqual(9, test_f.best_geos(self.blueprint_1))
        self.assertEqual(12, test_f.best_geos(self.blueprint_2))
        
    def test_values(self):
        test_f = Factario()
        test_f.load_file('test_input.txt')
        self.assertEqual(self.blueprint_1, test_f.blueprints[1])
        self.assertEqual(self.blueprint_2, test_f.blueprints[2])
        self.assertEqual(33, test_f.get_values())
        
    def test_part_2(self):
        test_f = Factario(32)
        test_f.load_file('test_input.txt')
        self.assertEqual(56, test_f.best_geos(self.blueprint_1))
        self.assertEqual(62, test_f.best_geos(self.blueprint_2))


class Factario:
    most_used: dict[str, int]
    blueprints: dict[int, dict[str, list[tuple[str, int]]]]
    
    def __init__(self, max_minutes = 24):
        self.max_minutes = max_minutes

    def load_file(self, filename: str):
        self.blueprints: dict[int, dict[str, list[tuple[str, int]]]] = {}
        pattern = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each "
                             r"obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and "
                             r"(\d+) obsidian.")
        with open(filename) as f:
            for line in f:
                match = pattern.search(line)
                self.blueprints[int(match[1])] = {
                    "ore_bot": [("ore", int(match[2]))],
                    "clay_bot": [("ore", int(match[3]))],
                    "obs_bot": [("ore", int(match[4])), ("clay", int(match[5]))],
                    "geo_bot": [("ore", int(match[6])), ("obs", int(match[7]))],
                }
    
    def get_values(self) -> int:
        total = 0
        for i, blueprint in self.blueprints.items():
            print(f"{i} * ", end='')
            total += i * self.best_geos(blueprint)
        return total
    
    def best_geos(self, blueprint: dict[str, list[tuple[str, int]]]) -> int:
        best_geo = 0
        best_plan = []
        
        self.most_used = {}
        for mat_list in blueprint.values():
            for mat, amt in mat_list:
                self.most_used[mat] = max(self.most_used.get(mat, 0), amt)
        
        plan: list[str] = []
        while self.get_next_plan(plan):
            material = {
                "ore": 0,
                "clay": 0,
                "obs": 0,
                "geo": 0,
            }
            bots = {
                "ore": 1,
                "clay": 0,
                "obs": 0,
                "geo": 0,
            }
            next_planned = 0
            for minute in range(1, self.max_minutes):
                # build the next bot if possible
                if len(plan) <= next_planned:
                    plan.append(self.next_best_bot(minute, material, bots))
                bot_type = plan[next_planned]
                build_bot = all(material[stuff] >= amt for stuff, amt in blueprint[bot_type])
                
                for stuff in material.keys():
                    material[stuff] += bots[stuff]
                
                if build_bot:
                    bots[bot_type.replace('_bot', '')] += 1
                    for stuff, amt in blueprint[bot_type]:
                        material[stuff] -= amt
                    next_planned += 1
            
            material['geo'] += bots['geo']  # last minute we don't build a bot
            if next_planned < len(plan) - 1:
                plan = plan[:next_planned]
            if material['geo'] > best_geo:
                best_geo = material['geo']
                best_plan = plan[:next_planned - 1]
        print(f'{best_geo}  {",".join(best_plan)}')
        return best_geo
    
    def get_next_plan(self, plan: list[str]) -> bool:
        if len(plan) == 0:
            plan.append('ore_bot')
            return True
        last_bot = plan.pop()
        while last_bot == 'geo_bot':
            last_bot = plan.pop()
        if last_bot == 'clay_bot' and len(plan) == 0:
            return False
        
        if last_bot == 'ore_bot':
            plan.append('clay_bot')
        elif last_bot == 'clay_bot':
            plan.append('obs_bot')
        else:
            plan.append('geo_bot')
        
        return True
    
    def next_best_bot(self, minute: int, material: dict[str, int], bots: dict[str, int]):
        if minute == self.max_minutes - 1:
            return 'geo_bot'
        
        remaining_minutes = self.max_minutes - 1 - minute
        # if there is a way to use up the rest of the ore in the time allowed, then add another ore_bot
        if material['ore'] + bots['ore'] * remaining_minutes < remaining_minutes * self.most_used['ore']:
            return 'ore_bot'
        if material['clay'] + bots['clay'] * remaining_minutes < remaining_minutes * self.most_used['clay']:
            return 'clay_bot'
        if material['obs'] + bots['obs'] * remaining_minutes < remaining_minutes * self.most_used['obs']:
            return 'obs_bot'
        return 'geo_bot'


if __name__ == '__main__':
    fact = Factario()
    fact.load_file('input.txt')
    print(fact.get_values())
    
    fact.max_minutes = 32
    start = time.monotonic()
    print(fact.best_geos(fact.blueprints[1]) * fact.best_geos(fact.blueprints[2]) * fact.best_geos(fact.blueprints[3]))
    print(time.monotonic() - start)
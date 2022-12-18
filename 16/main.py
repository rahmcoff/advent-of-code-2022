import unittest
import re


class TodayTest(unittest.TestCase):
    winning_path = ['DD', 'BB', 'JJ', 'HH', 'EE', 'CC']
    example_1_path = ['BB']
    example_2_path = ['BB', 'CC']
    
    def test_calulation(self):
        runner = ValveRunner()
        runner.load_file('test_input.txt')
        self.assertEqual(364, runner.calculate_flow(self.example_1_path))
        self.assertEqual((364 + 52), runner.calculate_flow(self.example_2_path))
        self.assertEqual(1651, runner.calculate_flow(self.winning_path))
    
    def test_part_1(self):
        runner = ValveRunner()
        runner.load_file('test_input.txt')
        self.assertEqual(1651, runner.get_most_flow())
    
    def test_part_2(self):
        runner = ValveRunner()
        runner.load_file('test_input.txt')
        self.assertEqual(1707, runner.get_double_flow())


class ValveRunner:
    valves: dict[str, int]
    graph: dict[str, list[str]]
    distances: dict[tuple[str, str], int]
    
    def load_file(self, filename):
        self.valves = {}
        self.graph = {}
        
        pattern = re.compile(r'Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)')
        with open(filename) as f:
            for line in f:
                match = pattern.match(line)
                room, flow, tunnels = match[1], int(match[2]), match[3]
                if flow > 0:
                    self.valves[room] = flow
                self.graph[room] = tunnels.split(', ')
        self.find_shortest_distances()
    
    def find_shortest_distances(self):
        self.distances = {}
        for to_valve in self.valves.keys():
            self.distances['AA', to_valve] = self.find_distance('AA', to_valve) + 1
            for from_valve in self.valves.keys():
                if from_valve == to_valve:
                    continue
                self.distances[from_valve, to_valve] = self.find_distance(from_valve, to_valve) + 1
    
    def find_distance(self, frm: str, to: str):
        node_cost: dict[str, int] = {frm: 0}
        boundary_nodes = [frm]
        
        while boundary_nodes:
            node = boundary_nodes.pop(0)
            if to in node_cost and node_cost[to] < node_cost[node] + 1:
                continue
            for next_node in self.graph[node]:
                if next_node not in node_cost or node_cost[next_node] > node_cost[node] + 1:
                    node_cost[next_node] = node_cost[node] + 1
                    boundary_nodes.append(next_node)
        return node_cost[to]
    
    def calculate_flow(self, path_to_valves: list[str], time=30):
        running_time = 0
        flow = 0
        for t, valve in enumerate(path_to_valves):
            if t == 0:
                prev_valve = 'AA'
            else:
                prev_valve = path_to_valves[t - 1]
            running_time += self.distances[prev_valve, valve]
            if running_time > time:
                return flow
            flow += (time - running_time) * self.valves[valve]
        return flow
    
    def get_most_flow(self, starting_list=['AA'], full_time=30, exclude_valves=[]) -> int:
        most_flow = 0
        
        prev_valve = starting_list[-1]
        for valve, flow in self.valves.items():
            if valve in starting_list or valve in exclude_valves:
                continue
            time_remaining = full_time - self.distances[prev_valve, valve]
            if time_remaining <= 0:
                continue
            this_flow = time_remaining * flow + self.get_most_flow(starting_list + [valve], time_remaining, exclude_valves)
            if this_flow > most_flow:
                most_flow = this_flow
        return most_flow
    
    def get_double_flow(self, starting_list=['AA'], full_time=26) -> int:
        most_flow = 0
        
        prev_valve = starting_list[-1]
        possible_valves = [v for v in self.valves.items() if v[0] not in starting_list]
        
        for valve, flow in possible_valves:
            remaining_time = full_time - self.distances[prev_valve, valve]
            if remaining_time <= 0:
                continue
            this_flow = self.get_double_flow(starting_list + [valve], remaining_time)
            this_flow += remaining_time * flow
            if this_flow > most_flow:
                most_flow = this_flow

        this_flow = self.get_most_flow(full_time=26, exclude_valves=starting_list)
        if this_flow > most_flow:
            most_flow = this_flow
            
        return most_flow


class StupidValveRunner:
    valves: dict[str, int]
    actions: dict[str, list[str]]
    minutes = 30
    
    def load_file(self, filename):
        self.valves = {}
        self.actions = {}
        pattern = re.compile(r'Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)')
        with open(filename) as f:
            for line in f:
                match = pattern.match(line)
                room, flow, tunnels = match[1], int(match[2]), match[3]
                if flow > 0:
                    self.valves[room] = flow
                    self.actions[room] = [f'turn on {room}']
                else:
                    self.actions[room] = []
                self.actions[room].extend(tunnels.split(', '))
    
    def get_most_flow(self) -> int:
        best_flow = 0
        flow = 0
        
        current_path: list[str] = []
        last_action: str | None = None
        remaining_valves = sum(self.valves.values())
        while True:
            while len(current_path) < self.minutes:
                actions = self.get_smart_actions(current_path)
                if not actions:
                    break
                if not last_action:
                    do_action = actions[0]
                else:
                    index = actions.index(last_action)
                    last_action = None
                    if index < len(actions) - 1:
                        do_action = actions[index + 1]
                    else:
                        break
                current_path.append(do_action)
                if len(do_action) > 2:
                    flow = self.calculate_flow(current_path)
                    if flow > best_flow:
                        print(','.join(current_path))
                        best_flow = flow
                    
                    remaining_valves -= self.valves[do_action[-2:]]
                
                if remaining_valves * (self.minutes - len(current_path)) <= best_flow - flow:
                    break
            
            if not current_path:
                break
            
            last_action = current_path.pop()
            if len(last_action) > 2:
                remaining_valves += self.valves[last_action[-2:]]
        
        return best_flow
    
    def get_smart_actions(self, path: list[str]) -> list[str]:
        if not path:
            return self.actions['AA'].copy()  # starting room
        room = path[-1][-2:]
        actions = self.actions[room].copy()
        
        if len(actions[0]) > 2 and actions[0] in path:  # If we’ve already turned on this valve, don’t do it again
            del actions[0]
        
        for i in range(len(path) - 1, -1,
                       -1):  # Don’t go back to a room we’ve ready been to since the last value was turned on
            if path[i][-2:] in actions:
                actions.remove(path[i][-2:])
            if len(path[i]) > 2:
                break
        return actions
    
    def calculate_flow(self, action_path) -> int:
        flow = 0
        for step, action in enumerate(action_path):
            if len(action) > 2:
                flow += (self.minutes - step - 1) * self.valves[action[-2:]]
        return flow
    
    def get_double_flow(self) -> int:
        best_flow = 0
        flow = 0
        self.minutes = 26
        
        current_path_1: list[str] = []
        current_path_2: list[str] = []
        last_action_1: str | None = None
        last_action_2: str | None = None
        remaining_valves = sum(self.valves.values())
        while True:
            while len(current_path_1) < self.minutes:
                actions_1, actions_2 = self.get_double_actions(current_path_1, current_path_2)
                
                if not actions_1 or not actions_2:
                    break
                if not last_action_1 or not last_action_2:
                    do_action_1 = actions_1[0]
                    do_action_2 = actions_2[0]
                else:
                    index_1 = actions_1.index(last_action_1)
                    index_2 = actions_2.index(last_action_2)
                    last_action_1 = last_action_2 = None
                    
                    if index_1 < len(actions_1) - 1:
                        do_action_1 = actions_1[index_1 + 1]
                        do_action_2 = actions_2[index_2]
                    elif index_2 < len(actions_2) - 1:
                        do_action_1 = actions_1[0]
                        do_action_2 = actions_2[index_2 + 1]
                    else:
                        break
                
                current_path_1.append(do_action_1)
                current_path_2.append(do_action_2)
                if len(do_action_1) > 2:
                    remaining_valves -= self.valves[do_action_1[-2:]]
                if len(do_action_2) > 2:
                    remaining_valves -= self.valves[do_action_2[-2:]]
                if len(do_action_1) > 2 or len(do_action_2) > 2:
                    flow = self.calculate_flow(current_path_1) + self.calculate_flow(current_path_2)
                    if flow > best_flow:
                        print(f"{','.join(current_path_1)} {','.join(current_path_2)}")
                        best_flow = flow
                
                if remaining_valves * (self.minutes - len(current_path_1)) <= best_flow - flow:
                    break
            
            if not current_path_1:
                break
            
            last_action_1 = current_path_1.pop()
            if len(last_action_1) > 2:
                remaining_valves += self.valves[last_action_1[-2:]]
            last_action_2 = current_path_2.pop()
            if len(last_action_2) > 2:
                remaining_valves += self.valves[last_action_2[-2:]]
        
        return best_flow
    
    def get_double_actions(self, current_path_1, current_path_2):
        actions_1 = self.get_smart_actions(current_path_1)
        actions_2 = self.get_smart_actions(current_path_2)
        
        if actions_1 and len(actions_1[0]) > 2 and actions_1[0] in current_path_2:
            del actions_1[0]
        if actions_2 and len(actions_2[0]) > 2 and actions_2[0] in current_path_1:
            del actions_2[0]
        if actions_1 and actions_2 and len(actions_2[0]) > 2 and actions_2[0] == actions_1[0]:
            del actions_2[0]
        
        return actions_1, actions_2


if __name__ == '__main__':
    runner = ValveRunner()
    runner.load_file('input.txt')
    print(runner.get_most_flow())
    print(runner.get_double_flow())

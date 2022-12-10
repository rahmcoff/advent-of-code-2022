import unittest


class TodayTest(unittest.TestCase):
    sample = ['addx 15', 'addx -11', 'addx 6', 'addx -3', 'addx 5', 'addx -1', 'addx -8', 'addx 13', 'addx 4', 'noop',
              'addx -1', 'addx 5', 'addx -1', 'addx 5', 'addx -1', 'addx 5', 'addx -1', 'addx 5', 'addx -1', 'addx -35',
              'addx 1', 'addx 24',
              'addx -19', 'addx 1', 'addx 16', 'addx -11', 'noop', 'noop', 'addx 21', 'addx -15', 'noop', 'noop',
              'addx -3', 'addx 9', 'addx 1',
              'addx -3', 'addx 8', 'addx 1', 'addx 5', 'noop', 'noop', 'noop', 'noop', 'noop', 'addx -36', 'noop',
              'addx 1', 'addx 7',
              'noop', 'noop', 'noop', 'addx 2', 'addx 6', 'noop', 'noop', 'noop', 'noop', 'noop', 'addx 1', 'noop',
              'noop', 'addx 7', 'addx 1',
              'noop', 'addx -13', 'addx 13', 'addx 7', 'noop', 'addx 1', 'addx -33', 'noop', 'noop', 'noop', 'addx 2',
              'noop', 'noop',
              'noop', 'addx 8', 'noop', 'addx -1', 'addx 2', 'addx 1', 'noop', 'addx 17', 'addx -9', 'addx 1', 'addx 1',
              'addx -3',
              'addx 11', 'noop', 'noop', 'addx 1', 'noop', 'addx 1', 'noop', 'noop', 'addx -13', 'addx -19', 'addx 1',
              'addx 3', 'addx 26', 'addx -30',
              'addx 12', 'addx -1', 'addx 3', 'addx 1', 'noop', 'noop', 'noop', 'addx -9', 'addx 18', 'addx 1',
              'addx 2', 'noop', 'noop',
              'addx 9', 'noop', 'noop', 'noop', 'addx -1', 'addx 2', 'addx -37', 'addx 1', 'addx 3', 'noop', 'addx 15',
              'addx -21', 'addx 22',
              'addx -6', 'addx 1', 'noop', 'addx 2', 'addx 1', 'noop', 'addx -10', 'noop', 'noop', 'addx 20', 'addx 1',
              'addx 2', 'addx 2',
              'addx -6', 'addx -11', 'noop', 'noop', 'noop']
    sample_values = [420, 1140, 1800, 2940, 2880, 3960]
    
    def test_get_values(self):
        self.assertEqual(self.sample_values, get_values(self.sample))
    
    sample_display = ['##..##..##..##..##..##..##..##..##..##..',
                      '###...###...###...###...###...###...###.',
                      '####....####....####....####....####....',
                      '#####.....#####.....#####.....#####.....',
                      '######......######......######......####',
                      '#######.......#######.......#######.....']
    
    def test_display(self):
        d = Display(self.sample)
        d.run_commands()
        self.assertEqual(self.sample_display, d.get_display())


def get_values(cmds: [str]) -> [int]:
    x = 1
    tick = 0
    values: [int] = []
    for op in cmds:
        op = op.strip()
        
        # The locgic is funky because it goes, update tick, then add
        if op == 'noop':
            tick += 1
        else:
            if tick % 40 == 19:
                values.append(x * (tick + 1))
            tick += 2
        
        if tick % 40 == 20:
            values.append(x * tick)
        
        if op[:5] == 'addx ':
            x += int(op[5:])
    return values


class Display:
    x = 1
    step = 0
    
    def __init__(self, cmds: [str]):
        self.cmds = [l.strip() for l in cmds]
        self.output: [str] = [' '] * 240
        
    def run_commands(self):
        for op in self.cmds:
            self.tick()
            if op[:5] == 'addx ':
                self.tick()
                self.x += int(op[5:])
                
    def tick(self):
        if abs(self.step % 40 - self.x) <= 1:
            self.output[self.step] = '#'
        else:
            self.output[self.step] = '.'
        self.step += 1
    
    def get_display(self) -> [str]:
        return [''.join(z) for z in zip(*[iter(self.output)]*40)]


if __name__ == '__main__':
    with open('input.txt') as f:
        program = f.readlines()
    
    print(sum(get_values(program)))
    
    disp = Display(program)
    disp.run_commands()
    for line in disp.get_display():
        print(line)

class Monkey:
    objects_seen = 0
    
    def __init__(self, starting: [int], operation: str, divisible: int, success_monkey: int, fail_monkey: int):
        self.objects = starting
        self.operation = operation
        self.divisible = divisible
        self.success_monkey = success_monkey
        self.fail_monkey = fail_monkey
    
    def process_next_object(self) -> (int, int):
        if not self.objects:
            return None
        
        self.objects_seen += 1
        worry_level = self.objects.pop(0)
        if self.operation == '* old':
            worry_level *= worry_level
        elif self.operation[:2] == '* ':
            worry_level *= int(self.operation[2:])
        elif self.operation[:2] == '+ ':
            worry_level += int(self.operation[2:])
        
        worry_level //= 3
        
        if worry_level % self.divisible == 0:
            return worry_level, self.success_monkey
        else:
            return worry_level, self.fail_monkey

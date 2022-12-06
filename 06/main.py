import unittest

class TestToday(unittest.TestCase):
    examples = [('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7, 19),
                ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5, 23),
                ('nppdvjthqldpwncqszvftbrmjlhg', 6, 23),
                ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10, 29),
                ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11, 26)]
    
    def test_find_start_of_packet(self):
        for e in self.examples:
            self.assertEqual(e[1], find_start_of_packet(e[0]))
            
    def test_find_message_length_14(self):
        for e in self.examples:
            self.assertEqual(e[2], find_start_of_packet(e[0], 14))
            
            
def find_start_of_packet(message_data: str, message_length=4) -> int:
    for i in range(message_length, len(message_data)):
        if len(set(message_data[i - message_length:i])) == message_length:
            return i
    

if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.readline().strip()
        
    print(find_start_of_packet(data))
    print(find_start_of_packet(data, 14), 14)


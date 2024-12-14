from random import randint

class Die:
    """一个骰子类"""
    def __init__(self, num_sides = 6) -> None:
        """骰子默认为6面"""
        self.num_sides = num_sides
        
    def roll(self):
        """返回一个介于1~骰子面数的随机值"""
        return randint(1, self.num_sides)
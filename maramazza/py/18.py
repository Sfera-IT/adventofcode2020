import re


class WiredOperator(int):
    def __add__(self, b):
        return WiredOperator(int(self) + b)

    def __mul__(self, b):
        return WiredOperator(int(self) + b)

    def __sub__(self, b):
        return WiredOperator(int(self) * b)


class Day18:
    def __init__(self, content):
        self.lines = content.split("\n")

    def part1(self):
        ans = 0
        for e in self.lines:
            e = re.sub(r"(\d)+", r"WiredOperator(\1)", e)
            e = e.replace("*", "-")
            v = eval(e, {}, {"WiredOperator": WiredOperator})
            ans += v
        return ans

    def part2(self):
        ans = 0
        for e in self.lines:
            e = re.sub(r"(\d+)", r"WiredOperator(\1)", e)
            e = e.replace("*", "-")
            e = e.replace("+", "*")
            v = eval(e, {}, {"WiredOperator": WiredOperator})
            ans += v
        return ans

def solve():
    content = open("./../data/18.txt").read()
    day18 = Day18(content)
    print(day18.part1())
    print(day18.part2())

solve()

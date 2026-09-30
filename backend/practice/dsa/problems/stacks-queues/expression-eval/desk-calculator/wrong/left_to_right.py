class Solution:
    # Mistake: ignores precedence and applies every operator left to right.
    def calculate(self, expr):
        total, num, op = 0, 0, "+"
        for c in expr + "+":
            if c == " ":
                continue
            if c.isdigit():
                num = num * 10 + ord(c) - 48
                continue
            if op == "+":
                total += num
            elif op == "-":
                total -= num
            elif op == "*":
                total *= num
            else:
                total = int(total / num)
            op, num = c, 0
        return total

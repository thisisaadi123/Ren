from fractions import Fraction


class Solution:
    def convoys(self, depot, position, speed):
        trucks = sorted(zip(position, speed), reverse=True)
        stack = []
        for p, s in trucks:
            t = Fraction(depot - p, s)
            if not stack or t > stack[-1]:
                stack.append(t)
        return len(stack)

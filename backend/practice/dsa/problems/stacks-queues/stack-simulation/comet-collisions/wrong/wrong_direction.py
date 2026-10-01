class Solution:
    # Mistake: also lets a right-moving comet hit a left-moving one on its left.
    def afterCollisions(self, comets):
        stack = []
        for c in comets:
            alive = True
            while alive and stack and (stack[-1] > 0) != (c > 0):
                if abs(stack[-1]) < abs(c):
                    stack.pop()
                elif abs(stack[-1]) == abs(c):
                    stack.pop()
                    alive = False
                else:
                    alive = False
            if alive:
                stack.append(c)
        return stack

class Solution:
    def afterCollisions(self, comets):
        stack = []
        for c in comets:
            alive = True
            while alive and c < 0 and stack and stack[-1] > 0:
                if stack[-1] < -c:
                    stack.pop()
                elif stack[-1] == -c:
                    stack.pop()
                    alive = False
                else:
                    alive = False
            if alive:
                stack.append(c)
        return stack

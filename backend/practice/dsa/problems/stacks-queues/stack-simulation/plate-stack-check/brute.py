class Solution:
    def couldHappen(self, washed, served):
        # Try every interleaving of pushes and pops (small inputs only).
        n = len(washed)

        def go(i, j, stack):
            if j == n:
                return True
            if stack and stack[-1] == served[j] and go(i, j + 1, stack[:-1]):
                return True
            return i < n and go(i + 1, j, stack + [washed[i]])

        return go(0, 0, [])

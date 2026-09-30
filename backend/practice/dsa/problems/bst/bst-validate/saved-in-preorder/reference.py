class Solution:
    def couldBePreorder(self, keys):
        low = -float("inf")
        stack = []
        for k in keys:
            if k < low:
                return False
            while stack and stack[-1] < k:
                low = stack.pop()
            stack.append(k)
        return True

class Solution:
    # Mistake: when the sequence climbs, uses the previous key as the lower bound instead of the last key popped.
    def couldBePreorder(self, keys):
        low = -float("inf")
        stack = []
        for i, k in enumerate(keys):
            if k < low:
                return False
            if stack and stack[-1] < k:
                low = keys[i - 1]
                while stack and stack[-1] < k:
                    stack.pop()
            stack.append(k)
        return True

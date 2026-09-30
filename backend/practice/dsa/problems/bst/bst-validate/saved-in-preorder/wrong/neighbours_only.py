class Solution:
    # Mistake: only checks that a key can hang below the key just before it.
    def couldBePreorder(self, keys):
        stack = []
        for k in keys:
            while stack and stack[-1] < k:
                stack.pop()
            stack.append(k)
        return True

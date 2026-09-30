class Solution:
    def canRepaint(self, s, t, m):
        if s == t:
            return True
        paint = {}
        for x, y in zip(s, t):
            if paint.setdefault(x, y) != y:
                return False
        return len(set(t)) < m

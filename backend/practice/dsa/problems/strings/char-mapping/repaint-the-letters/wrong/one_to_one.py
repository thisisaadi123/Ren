class Solution:
    # Mistake: demands a one-to-one map, but two colours may be merged into one.
    def canRepaint(self, s, t, m):
        if s == t:
            return True
        a, b = {}, {}
        for x, y in zip(s, t):
            if a.setdefault(x, y) != y or b.setdefault(y, x) != x:
                return False
        return len(set(t)) < m

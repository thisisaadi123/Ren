class Solution:
    # Mistake: forgets that zero steps are allowed, so s == t with every colour in use fails.
    def canRepaint(self, s, t, m):
        paint = {}
        for x, y in zip(s, t):
            if paint.setdefault(x, y) != y:
                return False
        return len(set(t)) < m

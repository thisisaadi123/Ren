class Solution:
    # Mistake: only checks that each colour lands on one colour, forgetting that swapping colours needs a spare one.
    def canRepaint(self, s, t, m):
        paint = {}
        for x, y in zip(s, t):
            if paint.setdefault(x, y) != y:
                return False
        return True

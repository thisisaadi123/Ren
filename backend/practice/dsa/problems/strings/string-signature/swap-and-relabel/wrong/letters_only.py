class Solution:
    # Mistake: checks the length and the set of letters, but not the counts.
    def canReshape(self, a, b):
        return len(a) == len(b) and set(a) == set(b)

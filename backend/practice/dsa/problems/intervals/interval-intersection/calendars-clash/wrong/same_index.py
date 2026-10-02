class Solution:
    # Mistake: only compares events at the same position in the two lists.
    def calendarsClash(self, a, b):
        return any(s1 < e2 and s2 < e1 for (s1, e1), (s2, e2) in zip(a, b))

class Solution:
    def calendarsClash(self, a, b):
        return any(s1 < e2 and s2 < e1 for s1, e1 in a for s2, e2 in b)

class Solution:
    # Mistake: compares every pair of events: O(n * m).
    def calendarsClash(self, a, b):
        for s1, e1 in a:
            for s2, e2 in b:
                if s1 < e2 and s2 < e1:
                    return True
        return False

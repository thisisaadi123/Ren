class Solution:
    # Mistake: counts one full set per right edge instead of every start that works.
    def countFullSets(self, s):
        last = {"a": -1, "b": -1, "c": -1}
        total = 0
        for i, c in enumerate(s):
            last[c] = i
            if min(last.values()) >= 0:
                total += 1
        return total

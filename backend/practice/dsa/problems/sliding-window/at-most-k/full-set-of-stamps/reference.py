class Solution:
    def countFullSets(self, s):
        last = {"a": -1, "b": -1, "c": -1}
        total = 0
        for i, c in enumerate(s):
            last[c] = i
            total += min(last.values()) + 1
        return total

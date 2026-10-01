class Solution:
    # Mistake: forgets the +1, losing the start at index min(...).
    def countFullSets(self, s):
        last = {"a": -1, "b": -1, "c": -1}
        total = 0
        for i, c in enumerate(s):
            last[c] = i
            total += max(0, min(last.values()))
        return total

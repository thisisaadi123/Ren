import itertools
class Solution:
    def widestSpacing(self, spots, sensors):
        best = 0
        for combo in itertools.combinations(sorted(spots), sensors):
            best = max(best, min(b - a for a, b in zip(combo, combo[1:])))
        return best

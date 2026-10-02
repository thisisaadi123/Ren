class Solution:
    def lampsAt(self, lamps, spots):
        return [sum(1 for s, e in lamps if s <= p <= e) for p in spots]

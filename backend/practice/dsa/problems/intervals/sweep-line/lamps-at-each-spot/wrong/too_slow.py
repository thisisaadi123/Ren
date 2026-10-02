class Solution:
    # Mistake: checks every lamp for every spot: O(n * q).
    def lampsAt(self, lamps, spots):
        out = []
        for p in spots:
            c = 0
            for s, e in lamps:
                if s <= p <= e:
                    c += 1
            out.append(c)
        return out

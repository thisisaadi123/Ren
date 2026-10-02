class Solution:
    def fewestPins(self, posters):
        from itertools import combinations
        cands = sorted({e for _, e in posters})
        for k in range(1, len(posters) + 1):
            for pick in combinations(cands, k):
                if all(any(s <= x <= e for x in pick) for s, e in posters):
                    return k
        return len(posters)

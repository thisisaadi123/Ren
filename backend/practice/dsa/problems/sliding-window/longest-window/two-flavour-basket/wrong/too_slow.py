class Solution:
    # Mistake: extends from every start: O(n^2) when long two-flavour stretches exist.
    def mostScoops(self, flavours):
        n = len(flavours)
        best = 0
        for i in range(n):
            seen = set()
            for j in range(i, n):
                seen.add(flavours[j])
                if len(seen) > 2:
                    break
                best = max(best, j - i + 1)
        return best

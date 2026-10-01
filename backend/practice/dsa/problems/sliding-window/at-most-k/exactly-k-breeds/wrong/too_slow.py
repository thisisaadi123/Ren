class Solution:
    # Mistake: extends from every start: O(n^2) when k is large.
    def countBreedStretches(self, pens, k):
        n = len(pens)
        total = 0
        for i in range(n):
            seen = set()
            for j in range(i, n):
                seen.add(pens[j])
                if len(seen) > k:
                    break
                if len(seen) == k:
                    total += 1
        return total

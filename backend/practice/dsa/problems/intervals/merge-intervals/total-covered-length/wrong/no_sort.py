class Solution:
    # Mistake: merges in the given order without sorting.
    def coveredLength(self, strips):
        total, cur = 0, None
        for s, e in strips:
            if cur and cur[0] <= s <= cur[1]:
                cur[1] = max(cur[1], e)
            else:
                if cur:
                    total += cur[1] - cur[0]
                cur = [s, e]
        return total + cur[1] - cur[0]

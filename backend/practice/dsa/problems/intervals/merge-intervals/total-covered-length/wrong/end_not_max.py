class Solution:
    # Mistake: a strip inside the current one cuts the current one short.
    def coveredLength(self, strips):
        total, cur = 0, None
        for s, e in sorted(strips):
            if cur and s <= cur[1]:
                cur[1] = e
            else:
                if cur:
                    total += cur[1] - cur[0]
                cur = [s, e]
        return total + cur[1] - cur[0]

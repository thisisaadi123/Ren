class Solution:
    def coveredLength(self, strips):
        total, cur = 0, None
        for s, e in sorted(strips):
            if cur and s <= cur[1]:
                cur[1] = max(cur[1], e)
            else:
                if cur:
                    total += cur[1] - cur[0]
                cur = [s, e]
        return total + cur[1] - cur[0]

class Solution:
    def coveredLength(self, strips):
        points = sorted({p for s in strips for p in s})
        total = 0
        for a, b in zip(points, points[1:]):
            if any(s <= a and b <= e for s, e in strips):
                total += b - a
        return total

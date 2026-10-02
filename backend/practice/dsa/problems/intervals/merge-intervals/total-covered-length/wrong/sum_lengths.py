class Solution:
    # Mistake: adds every strip's length, counting overlaps twice.
    def coveredLength(self, strips):
        return sum(e - s for s, e in strips)

class Solution:
    # Mistake: forgets the k limit and pairs posts at any distance.
    def bestPair(self, posts, k):
        best = None
        top = None
        for x, y in posts:
            if top is not None:
                v = y + x + top
                if best is None or v > best:
                    best = v
            if top is None or y - x > top:
                top = y - x
        return best

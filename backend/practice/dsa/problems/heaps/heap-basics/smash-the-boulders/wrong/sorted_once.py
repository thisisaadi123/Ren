class Solution:
    # Mistake: sorts once and smashes in that order, ignoring the new pieces' sizes.
    def lastBoulder(self, boulders):
        xs = sorted(boulders)
        while len(xs) > 1:
            a, b = xs.pop(), xs.pop()
            if a != b:
                xs.insert(0, a - b)
        return xs[0] if xs else 0

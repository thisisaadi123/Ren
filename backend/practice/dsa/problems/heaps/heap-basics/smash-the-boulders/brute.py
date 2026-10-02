class Solution:
    def lastBoulder(self, boulders):
        xs = list(boulders)
        while len(xs) > 1:
            xs.sort()
            a, b = xs.pop(), xs.pop()
            if a != b:
                xs.append(a - b)
        return xs[0] if xs else 0

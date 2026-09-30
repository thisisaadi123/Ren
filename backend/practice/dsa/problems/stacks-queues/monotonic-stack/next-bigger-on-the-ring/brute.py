class Solution:
    def nextBiggerOnRing(self, ring):
        n = len(ring)
        res = []
        for i in range(n):
            res.append(next((ring[(i + d) % n] for d in range(1, n) if ring[(i + d) % n] > ring[i]), -1))
        return res

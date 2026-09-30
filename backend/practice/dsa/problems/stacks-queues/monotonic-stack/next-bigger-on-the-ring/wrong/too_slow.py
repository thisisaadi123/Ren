class Solution:
    # Mistake: walks the ring from every tile: O(n²) when bigger tiles are rare.
    def nextBiggerOnRing(self, ring):
        n = len(ring)
        res = [-1] * n
        for i in range(n):
            for d in range(1, n):
                if ring[(i + d) % n] > ring[i]:
                    res[i] = ring[(i + d) % n]
                    break
        return res

class Solution:
    def nextBiggerOnRing(self, ring):
        n = len(ring)
        res = [-1] * n
        st = []
        for i in range(2 * n):
            v = ring[i % n]
            while st and ring[st[-1]] < v:
                res[st.pop()] = v
            if i < n:
                st.append(i)
        return res

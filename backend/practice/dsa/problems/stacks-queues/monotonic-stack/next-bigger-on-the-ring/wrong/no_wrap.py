class Solution:
    # Mistake: forgets the ring wraps around, so tiles near the end miss bigger tiles at the start.
    def nextBiggerOnRing(self, ring):
        res = [-1] * len(ring)
        st = []
        for i, v in enumerate(ring):
            while st and ring[st[-1]] < v:
                res[st.pop()] = v
            st.append(i)
        return res

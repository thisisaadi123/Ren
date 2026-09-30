class Solution:
    # Mistake: counts the shorter people but forgets the first taller person, who is visible too.
    def canSee(self, heights):
        n = len(heights)
        res = [0] * n
        st = []
        for i in range(n - 1, -1, -1):
            h, c = heights[i], 0
            while st and st[-1] < h:
                st.pop()
                c += 1
            if st and st[-1] == h:
                st.pop()
            st.append(h)
            res[i] = c
        return res

class Solution:
    def biggestBillboard(self, heights):
        best = 0
        st = []
        for i, h in enumerate(heights + [0]):
            while st and heights[st[-1]] >= h:
                top = heights[st.pop()]
                left = st[-1] if st else -1
                best = max(best, top * (i - left - 1))
            st.append(i)
        return best

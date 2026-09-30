class Solution:
    # Mistake: forgets to empty the stack at the end, missing billboards that reach the last building.
    def biggestBillboard(self, heights):
        best = 0
        st = []
        for i, h in enumerate(heights):
            while st and heights[st[-1]] >= h:
                top = heights[st.pop()]
                left = st[-1] if st else -1
                best = max(best, top * (i - left - 1))
            st.append(i)
        return best

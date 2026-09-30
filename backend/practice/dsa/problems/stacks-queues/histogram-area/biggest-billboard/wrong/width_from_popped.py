class Solution:
    # Mistake: measures the width from the popped index, ignoring taller buildings popped before it.
    def biggestBillboard(self, heights):
        best = 0
        st = []
        for i, h in enumerate(heights + [0]):
            while st and heights[st[-1]] >= h:
                j = st.pop()
                best = max(best, heights[j] * (i - j))
            st.append(i)
        return best

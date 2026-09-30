class Solution:
    # Mistake: lets the third value tie with the first or the second.
    def hasLowHighBetween(self, values):
        mid = float("-inf")
        st = []
        for v in reversed(values):
            if v <= mid:
                return True
            while st and st[-1] <= v:
                mid = st.pop()
            st.append(v)
        return False

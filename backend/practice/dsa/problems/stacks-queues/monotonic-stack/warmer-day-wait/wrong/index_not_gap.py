class Solution:
    # Mistake: records the index of the warmer day instead of how many days away it is.
    def daysUntilWarmer(self, temps):
        res = [0] * len(temps)
        st = []
        for i, t in enumerate(temps):
            while st and temps[st[-1]] < t:
                res[st.pop()] = i
            st.append(i)
        return res

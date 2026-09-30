class Solution:
    # Mistake: treats an equally warm day as warmer.
    def daysUntilWarmer(self, temps):
        res = [0] * len(temps)
        st = []
        for i, t in enumerate(temps):
            while st and temps[st[-1]] <= t:
                j = st.pop()
                res[j] = i - j
            st.append(i)
        return res

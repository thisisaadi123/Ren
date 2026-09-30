class Solution:
    # Mistake: for each middle only tries the first smaller value after it.
    def hasLowHighBetween(self, values):
        n = len(values)
        nxt = [None] * n
        st = []
        for i in range(n):
            while st and values[st[-1]] > values[i]:
                nxt[st.pop()] = values[i]
            st.append(i)
        low = float("inf")
        for j in range(n):
            if nxt[j] is not None and low < nxt[j]:
                return True
            low = min(low, values[j])
        return False

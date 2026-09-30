class Solution:
    # Mistake: forgets to drop leading zeros.
    def trimReading(self, num, k):
        st = []
        for d in num:
            while k and st and st[-1] > d:
                st.pop()
                k -= 1
            st.append(d)
        if k:
            st = st[:-k]
        return "".join(st) or "0"

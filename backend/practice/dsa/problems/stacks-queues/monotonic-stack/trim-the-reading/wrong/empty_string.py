class Solution:
    # Mistake: returns "" instead of "0" when nothing is left.
    def trimReading(self, num, k):
        st = []
        for d in num:
            while k and st and st[-1] > d:
                st.pop()
                k -= 1
            st.append(d)
        if k:
            st = st[:-k]
        return "".join(st).lstrip("0")

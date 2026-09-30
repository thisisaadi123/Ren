class Solution:
    # Mistake: when the digits never fall, the unused deletions are never spent.
    def trimReading(self, num, k):
        st = []
        for d in num:
            while k and st and st[-1] > d:
                st.pop()
                k -= 1
            st.append(d)
        return "".join(st).lstrip("0") or "0"

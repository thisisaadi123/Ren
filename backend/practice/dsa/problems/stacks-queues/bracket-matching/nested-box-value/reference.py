class Solution:
    def boxValue(self, s):
        MOD = 10**9 + 7
        st = [0]
        for c in s:
            if c == "(":
                st.append(0)
            else:
                t = st.pop()
                st[-1] = (st[-1] + (1 if t == 0 else 2 * t)) % MOD
        return st[0]

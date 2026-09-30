class Solution:
    # Mistake: forgets the modulo, so the value overflows on deep nesting.
    def boxValue(self, s):
        st = [0]
        for c in s:
            if c == "(":
                st.append(0)
            else:
                t = st.pop()
                st[-1] = (st[-1] + (1 if t == 0 else 2 * t)) & 0xFFFFFFFFFFFFFFFF
        return st[0]

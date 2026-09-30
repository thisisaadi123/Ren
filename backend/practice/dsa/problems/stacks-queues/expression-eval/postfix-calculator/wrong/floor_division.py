class Solution:
    # Mistake: uses floor division, so -7 / 2 gives -4 instead of -3.
    def evalPostfix(self, tokens):
        st = []
        for t in tokens:
            if t in ("+", "-", "*", "/"):
                b = st.pop()
                a = st.pop()
                st.append(a + b if t == "+" else a - b if t == "-" else a * b if t == "*" else a // b)
            else:
                st.append(int(t))
        return st[0]

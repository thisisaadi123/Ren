class Solution:
    # Mistake: pops a first, then b, so subtraction and division run backwards.
    def evalPostfix(self, tokens):
        st = []
        for t in tokens:
            if t in ("+", "-", "*", "/"):
                a = st.pop()
                b = st.pop()
                if t == "/":
                    q = abs(a) // abs(b)
                    st.append(q if (a < 0) == (b < 0) else -q)
                else:
                    st.append(a + b if t == "+" else a - b if t == "-" else a * b)
            else:
                st.append(int(t))
        return st[0]

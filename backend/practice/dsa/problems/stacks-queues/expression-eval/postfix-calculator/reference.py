class Solution:
    def evalPostfix(self, tokens):
        st = []
        for t in tokens:
            if t in ("+", "-", "*", "/"):
                b = st.pop()
                a = st.pop()
                if t == "+":
                    st.append(a + b)
                elif t == "-":
                    st.append(a - b)
                elif t == "*":
                    st.append(a * b)
                else:
                    q = abs(a) // abs(b)
                    st.append(q if (a < 0) == (b < 0) else -q)
            else:
                st.append(int(t))
        return st[0]

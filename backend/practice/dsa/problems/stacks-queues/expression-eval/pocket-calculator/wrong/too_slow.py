class Solution:
    # Mistake: for every "(" scans ahead for its partner and re-evaluates the slice recursively: O(n · depth).
    def evaluate(self, expr):
        def ev(s):
            st, num, op, i, n = [], 0, "+", 0, len(s)
            while i <= n:
                c = s[i] if i < n else "#"
                if c == " ":
                    i += 1
                    continue
                if c.isdigit():
                    num = num * 10 + ord(c) - 48
                    i += 1
                    continue
                if c == "(":
                    d, j = 0, i
                    while True:
                        d += (s[j] == "(") - (s[j] == ")")
                        if d == 0:
                            break
                        j += 1
                    num = ev(s[i + 1:j])
                    i = j + 1
                    continue
                if op == "+":
                    st.append(num)
                elif op == "-":
                    st.append(-num)
                elif op == "*":
                    st[-1] *= num
                else:
                    q = abs(st[-1]) // abs(num)
                    st[-1] = q if (st[-1] < 0) == (num < 0) else -q
                op, num = c, 0
                i += 1
            return sum(st)
        return ev(expr)

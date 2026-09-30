class Solution:
    # Mistake: only handles a number when an operator follows it, so the last number is lost.
    def calculate(self, expr):
        st, num, op = [], 0, "+"
        for c in expr:
            if c == " ":
                continue
            if c.isdigit():
                num = num * 10 + ord(c) - 48
                continue
            if op == "+":
                st.append(num)
            elif op == "-":
                st.append(-num)
            elif op == "*":
                st[-1] *= num
            else:
                q = abs(st[-1]) // num
                st[-1] = q if st[-1] >= 0 else -q
            op, num = c, 0
        return sum(st)

class Solution:
    # Mistake: after ")" the level resumes with "+", forgetting the operator that came before "(".
    def evaluate(self, expr):
        frames = []
        st, op, num = [], "+", 0
        for c in expr + "#":
            if c == " ":
                continue
            if c.isdigit():
                num = num * 10 + ord(c) - 48
                continue
            if c == "(":
                frames.append(st)
                st, op, num = [], "+", 0
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
            if c == ")":
                num = sum(st)
                st, op = frames.pop(), "+"
            else:
                op, num = c, 0
        return sum(st)

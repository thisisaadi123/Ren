class Solution:
    # Mistake: floor division on a negative stack top rounds the wrong way (1-7/2 gives -3).
    def calculate(self, expr):
        st, num, op = [], 0, "+"
        for c in expr + "+":
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
                st[-1] //= num
            op, num = c, 0
        return sum(st)

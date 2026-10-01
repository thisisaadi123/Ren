class Solution:
    # Mistake: reads only the last digit of a repeat count.
    def expand(self, pattern):
        stack = []
        cur, num = [], 0
        for c in pattern:
            if c.isdigit():
                num = int(c)
            elif c == "[":
                stack.append((cur, num))
                cur, num = [], 0
            elif c == "]":
                prev, k = stack.pop()
                prev.append("".join(cur) * k)
                cur = prev
            else:
                cur.append(c)
        return "".join(cur)

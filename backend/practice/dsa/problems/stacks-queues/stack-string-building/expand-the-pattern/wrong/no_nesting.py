class Solution:
    # Mistake: forgets the text before an inner group, so nested groups lose what came before them.
    def expand(self, pattern):
        stack = []
        cur, num = [], 0
        for c in pattern:
            if c.isdigit():
                num = num * 10 + int(c)
            elif c == "[":
                stack.append(num)
                cur, num = [], 0
            elif c == "]":
                cur = ["".join(cur) * stack.pop()]
            else:
                cur.append(c)
        return "".join(cur)

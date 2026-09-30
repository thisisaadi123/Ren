class Solution:
    def boxValue(self, s):
        def value(t):
            total, depth, start = 0, 0, 0
            for i, c in enumerate(t):
                depth += 1 if c == "(" else -1
                if depth == 0:
                    inner = t[start + 1:i]
                    total += 1 if not inner else 2 * value(inner)
                    start = i + 1
            return total
        return value(s) % (10**9 + 7)

class Solution:
    def longestBalanced(self, s):
        def ok(t):
            d = 0
            for c in t:
                d += 1 if c == "(" else -1
                if d < 0:
                    return False
            return d == 0
        n = len(s)
        for length in range(n - n % 2, 0, -2):
            for i in range(n - length + 1):
                if ok(s[i:i + length]):
                    return length
        return 0

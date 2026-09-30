class Solution:
    # Mistake: splits the string into top-level boxes and recurses into each: O(n · depth).
    def boxValue(self, s):
        MOD = 10**9 + 7
        def value(t):
            total, depth, start = 0, 0, 0
            for i, c in enumerate(t):
                depth += 1 if c == "(" else -1
                if depth == 0:
                    total += 1 if i == start + 1 else 2 * value(t[start + 1:i])
                    start = i + 1
            return total % MOD
        return value(s)

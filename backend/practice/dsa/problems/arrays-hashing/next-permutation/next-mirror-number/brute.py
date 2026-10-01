from itertools import permutations


class Solution:
    def nextMirror(self, code):
        if len(code) <= 8:
            best = None
            for p in set(permutations(code)):
                s = "".join(p)
                if s[0] != "0" and s == s[::-1] and s > code and (best is None or s < best):
                    best = s
            return best or ""
        n = len(code)
        half = code[:n // 2]
        for i in range(len(half) - 2, -1, -1):
            bigger = [c for c in half[i + 1:] if c > half[i]]
            if bigger:
                d = min(bigger)
                rest = list(half[i:])
                rest.remove(d)
                left = half[:i] + d + "".join(sorted(rest))
                return left + code[n // 2:(n + 1) // 2] + left[::-1]
        return ""

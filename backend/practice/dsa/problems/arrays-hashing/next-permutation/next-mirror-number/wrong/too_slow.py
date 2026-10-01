class Solution:
    # Mistake: rescans the rest of the half for every position: O(n^2).
    def nextMirror(self, code):
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

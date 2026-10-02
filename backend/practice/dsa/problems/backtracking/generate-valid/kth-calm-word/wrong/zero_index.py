class Solution:
    # Mistake: treats k as 0-indexed.
    def kthCalmWord(self, n, k):
        if k >= 3 << (n - 1):
            return ""
        out = []
        for i in range(n):
            block = 1 << (n - 1 - i)
            opts = [c for c in "abc" if not out or c != out[-1]]
            out.append(opts[k // block])
            k %= block
        return "".join(out)

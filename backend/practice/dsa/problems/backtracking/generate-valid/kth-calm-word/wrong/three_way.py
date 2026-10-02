class Solution:
    # Mistake: splits every position into three blocks, as if repeats were allowed.
    def kthCalmWord(self, n, k):
        if k > 3 << (n - 1):
            return ""
        k -= 1
        out = []
        for i in range(n):
            block = 3 ** (n - 1 - i)
            opts = [c for c in "abc" if not out or c != out[-1]]
            out.append(opts[min(len(opts) - 1, k // block)])
            k %= block
        return "".join(out)

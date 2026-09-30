class Solution:
    def kthOfTwo(self, a, b, k):
        if len(a) > len(b):
            a, b = b, a
        m, n = len(a), len(b)
        lo, hi = max(0, k - n), min(k, m)  # how many values come from a
        while lo < hi:
            i = (lo + hi) // 2
            j = k - i
            if a[i] < b[j - 1]:
                lo = i + 1
            else:
                hi = i
        i, j = lo, k - lo
        return max(a[i - 1] if i > 0 else -float("inf"), b[j - 1] if j > 0 else -float("inf"))

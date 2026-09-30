class Solution:
    def sharedTune(self, a, b):
        M, B = (1 << 61) - 1, 1000003

        def prefix(s):
            pre = [0] * (len(s) + 1)
            for i, c in enumerate(s):
                pre[i + 1] = (pre[i] * B + ord(c)) % M
            return pre

        pa, pb = prefix(a), prefix(b)
        m = max(len(a), len(b))
        pw = [1] * (m + 1)
        for i in range(m):
            pw[i + 1] = pw[i] * B % M

        def shared(L):
            p = pw[L]
            seen = {}
            for i in range(len(a) - L + 1):
                seen.setdefault((pa[i + L] - pa[i] * p) % M, i)
            for j in range(len(b) - L + 1):
                i = seen.get((pb[j + L] - pb[j] * p) % M)
                if i is not None and a[i:i + L] == b[j:j + L]:
                    return True
            return False

        lo, hi = 0, min(len(a), len(b))
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if shared(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo

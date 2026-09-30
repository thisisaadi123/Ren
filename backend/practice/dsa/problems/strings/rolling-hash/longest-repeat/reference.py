class Solution:
    def longestRepeat(self, s):
        n = len(s)
        M, B = (1 << 61) - 1, 911382323
        a = [ord(c) - 96 for c in s]
        pre = [0] * (n + 1)
        pw = [1] * (n + 1)
        for i in range(n):
            pre[i + 1] = (pre[i] * B + a[i]) % M
            pw[i + 1] = pw[i] * B % M

        def repeats(L):
            seen = {}
            p = pw[L]
            for i in range(n - L + 1):
                h = (pre[i + L] - pre[i] * p) % M
                j = seen.get(h)
                if j is not None and s[j:j + L] == s[i:i + L]:
                    return True
                seen.setdefault(h, i)
            return False

        lo, hi = 0, n - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if repeats(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo

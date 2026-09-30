class Solution:
    def committeePicks(self, n, k):
        out = []
        for mask in range(1 << n):
            if bin(mask).count("1") == k:
                out.append([i + 1 for i in range(n) if mask >> i & 1])
        return out

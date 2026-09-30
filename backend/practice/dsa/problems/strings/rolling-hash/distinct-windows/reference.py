class Solution:
    def distinctWindows(self, s, k):
        M1, M2, B = (1 << 61) - 1, 10**9 + 7, 131
        n = len(s)
        p1, p2 = pow(B, k - 1, M1), pow(B, k - 1, M2)
        h1 = h2 = 0
        for i in range(k):
            c = ord(s[i])
            h1 = (h1 * B + c) % M1
            h2 = (h2 * B + c) % M2
        seen = {(h1, h2)}
        for i in range(k, n):
            out, c = ord(s[i - k]), ord(s[i])
            h1 = ((h1 - out * p1) * B + c) % M1
            h2 = ((h2 - out * p2) * B + c) % M2
            seen.add((h1, h2))
        return len(seen)

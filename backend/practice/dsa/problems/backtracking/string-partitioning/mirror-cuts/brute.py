class Solution:
    def mirrorCuts(self, s):
        n = len(s)
        out = []
        for mask in range(1 << (n - 1)):
            pieces, start = [], 0
            for i in range(1, n):
                if mask >> (i - 1) & 1:
                    pieces.append(s[start:i])
                    start = i
            pieces.append(s[start:])
            if all(p == p[::-1] for p in pieces):
                out.append(pieces)
        return sorted(out)

class Solution:
    def mostPieces(self, s):
        n = len(s)
        best = 1
        for mask in range(1 << (n - 1)):
            pieces, start = [], 0
            for i in range(1, n):
                if mask >> (i - 1) & 1:
                    pieces.append(s[start:i])
                    start = i
            pieces.append(s[start:])
            if len(set(pieces)) == len(pieces):
                best = max(best, len(pieces))
        return best

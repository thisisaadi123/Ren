class Solution:
    def repeatWithinReach(self, codes, k):
        n = len(codes)
        return any(codes[i] == codes[j] for i in range(n) for j in range(i + 1, min(n, i + k + 1)))

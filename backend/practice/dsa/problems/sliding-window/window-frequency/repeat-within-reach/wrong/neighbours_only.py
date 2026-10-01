class Solution:
    # Mistake: only compares neighbouring codes.
    def repeatWithinReach(self, codes, k):
        return k >= 1 and any(codes[i] == codes[i + 1] for i in range(len(codes) - 1))

class Solution:
    def repeatWithinReach(self, codes, k):
        window = set()
        for i, c in enumerate(codes):
            if c in window:
                return True
            window.add(c)
            if i >= k:
                window.discard(codes[i - k])
        return False

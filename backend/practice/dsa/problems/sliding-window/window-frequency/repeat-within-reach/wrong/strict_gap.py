class Solution:
    # Mistake: requires the repeats to be strictly fewer than k apart.
    def repeatWithinReach(self, codes, k):
        window = set()
        for i, c in enumerate(codes):
            if c in window:
                return True
            window.add(c)
            if i >= k - 1:
                window.discard(codes[i - k + 1])
        return False

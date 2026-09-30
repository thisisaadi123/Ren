class Solution:
    # Mistake: counts pairs of identical substrings, missing rearranged ones.
    def anagramTwins(self, s):
        n, total = len(s), 0
        for L in range(1, n):
            seen = collections.Counter(s[i:i + L] for i in range(n - L + 1))
            total += sum(c * (c - 1) // 2 for c in seen.values())
        return total

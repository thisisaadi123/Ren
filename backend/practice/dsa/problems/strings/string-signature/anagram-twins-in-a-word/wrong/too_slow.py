class Solution:
    # Compares every pair of same-length substrings: O(n³) comparisons.
    def anagramTwins(self, s):
        n, total = len(s), 0
        for L in range(1, n):
            keys = ["".join(sorted(s[i:i + L])) for i in range(n - L + 1)]
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    if keys[i] == keys[j]:
                        total += 1
        return total

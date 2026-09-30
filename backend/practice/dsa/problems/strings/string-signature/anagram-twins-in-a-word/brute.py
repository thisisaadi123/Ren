class Solution:
    def anagramTwins(self, s):
        n, total = len(s), 0
        for L in range(1, n + 1):
            for i in range(n - L + 1):
                for j in range(i + 1, n - L + 1):
                    if sorted(s[i:i + L]) == sorted(s[j:j + L]):
                        total += 1
        return total

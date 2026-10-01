class Solution:
    # Mistake: tries every start and extends it: O(n^2).
    def longestUniform(self, s, k):
        best = 0
        for i in range(len(s)):
            count = [0] * 26
            mx = 0
            for j in range(i, len(s)):
                x = ord(s[j]) - 65
                count[x] += 1
                mx = max(mx, count[x])
                if j - i + 1 - mx > k:
                    break
                best = max(best, j - i + 1)
        return best

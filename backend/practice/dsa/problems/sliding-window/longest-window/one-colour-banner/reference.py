class Solution:
    def longestUniform(self, s, k):
        count = [0] * 26
        left = maxf = best = 0
        for i, c in enumerate(s):
            x = ord(c) - 65
            count[x] += 1
            maxf = max(maxf, count[x])
            while i - left + 1 - maxf > k:
                count[ord(s[left]) - 65] -= 1
                left += 1
            best = max(best, i - left + 1)
        return best

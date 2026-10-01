class Solution:
    # Mistake: always repaints to the window's FIRST letter instead of its most common one.
    def longestUniform(self, s, k):
        best = left = 0
        for i in range(len(s)):
            while sum(1 for c in s[left:i + 1] if c != s[left]) > k:
                left += 1
            best = max(best, i - left + 1)
        return best

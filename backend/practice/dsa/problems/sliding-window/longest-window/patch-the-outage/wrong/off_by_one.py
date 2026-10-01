class Solution:
    # Mistake: shrinks while zeros >= k, so it only ever keeps k - 1 patched minutes.
    def longestOnline(self, status, k):
        left = zeros = best = 0
        for i, v in enumerate(status):
            if v == 0:
                zeros += 1
            while zeros >= k and left <= i and zeros > 0:
                if status[left] == 0:
                    zeros -= 1
                left += 1
            best = max(best, i - left + 1)
        return best

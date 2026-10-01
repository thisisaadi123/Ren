class Solution:
    def longestOnline(self, status, k):
        left = zeros = best = 0
        for i, v in enumerate(status):
            if v == 0:
                zeros += 1
            while zeros > k:
                if status[left] == 0:
                    zeros -= 1
                left += 1
            best = max(best, i - left + 1)
        return best

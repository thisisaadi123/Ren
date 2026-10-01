class Solution:
    # Mistake: when too many zeros pile up, restarts the window at the current minute.
    def longestOnline(self, status, k):
        left = zeros = best = 0
        for i, v in enumerate(status):
            if v == 0:
                zeros += 1
            if zeros > k:
                left = i
                zeros = 1 if v == 0 else 0
                if zeros > k:
                    left, zeros = i + 1, 0
            best = max(best, i - left + 1)
        return best

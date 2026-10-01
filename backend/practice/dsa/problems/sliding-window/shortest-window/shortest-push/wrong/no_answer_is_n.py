class Solution:
    # Mistake: returns the length of the whole log when no stretch gets there.
    def shortestPush(self, gains, target):
        left = total = 0
        best = len(gains)
        for i, g in enumerate(gains):
            total += g
            while total >= target:
                best = min(best, i - left + 1)
                total -= gains[left]
                left += 1
        return best

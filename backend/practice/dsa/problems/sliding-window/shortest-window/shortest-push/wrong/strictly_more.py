class Solution:
    # Mistake: needs the total to go strictly past the target.
    def shortestPush(self, gains, target):
        left = total = 0
        best = len(gains) + 1
        for i, g in enumerate(gains):
            total += g
            while total > target:
                best = min(best, i - left + 1)
                total -= gains[left]
                left += 1
        return best if best <= len(gains) else 0

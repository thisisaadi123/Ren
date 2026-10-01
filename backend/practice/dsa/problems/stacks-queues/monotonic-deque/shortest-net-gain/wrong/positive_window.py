class Solution:
    # Mistake: uses the shrink-while-big-enough window, which assumes every change is positive.
    def shortestNetGain(self, changes, target):
        left = total = 0
        best = len(changes) + 1
        for i, v in enumerate(changes):
            total += v
            while left <= i and total >= target:
                best = min(best, i - left + 1)
                total -= changes[left]
                left += 1
        return best if best <= len(changes) else -1

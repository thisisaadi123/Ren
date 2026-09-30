class Solution:
    # Mistake: assumes the duplicate is the largest repeated-looking value from sums alone.
    def findMislabel(self, labels):
        n = len(labels)
        diff = sum(labels) - n * (n + 1) // 2
        dup = max(labels)
        return [dup, dup - diff]

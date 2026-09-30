class Solution:
    # Mistake: assumes the repeat appears exactly twice and every other number exactly once.
    def findRepeat(self, tickets):
        n = len(tickets) - 1
        return sum(tickets) - n * (n + 1) // 2

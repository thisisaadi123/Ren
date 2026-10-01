class Solution:
    # Mistake: counts one stretch per right edge, ignoring the even numbers that can be dropped from the left.
    def countOddStretches(self, tickets, k):
        left = odd = total = 0
        for i, v in enumerate(tickets):
            odd += v & 1
            while odd > k:
                odd -= tickets[left] & 1
                left += 1
            if odd == k:
                total += 1
        return total

class Solution:
    # Mistake: counts stretches with AT MOST k odd numbers.
    def countOddStretches(self, tickets, k):
        left = odd = total = 0
        for i, v in enumerate(tickets):
            odd += v & 1
            while odd > k:
                odd -= tickets[left] & 1
                left += 1
            total += i - left + 1
        return total

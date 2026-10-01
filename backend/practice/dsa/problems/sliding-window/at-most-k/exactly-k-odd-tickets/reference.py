class Solution:
    def countOddStretches(self, tickets, k):
        def at_most(limit):
            left = odd = total = 0
            for i, v in enumerate(tickets):
                odd += v & 1
                while odd > limit:
                    odd -= tickets[left] & 1
                    left += 1
                total += i - left + 1
            return total

        return at_most(k) - at_most(k - 1)

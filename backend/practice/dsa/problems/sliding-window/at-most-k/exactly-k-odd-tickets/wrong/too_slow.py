class Solution:
    # Mistake: extends from every start: O(n^2) when odd numbers are rare.
    def countOddStretches(self, tickets, k):
        n = len(tickets)
        total = 0
        for i in range(n):
            odd = 0
            for j in range(i, n):
                odd += tickets[j] & 1
                if odd > k:
                    break
                if odd == k:
                    total += 1
        return total

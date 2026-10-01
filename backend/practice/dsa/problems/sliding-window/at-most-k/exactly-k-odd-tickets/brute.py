class Solution:
    def countOddStretches(self, tickets, k):
        n = len(tickets)
        return sum(1 for i in range(n) for j in range(i, n) if sum(v & 1 for v in tickets[i:j + 1]) == k)

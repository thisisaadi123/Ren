class Solution:
    def shortestPush(self, gains, target):
        n = len(gains)
        for length in range(1, n + 1):
            if any(sum(gains[i:i + length]) >= target for i in range(n - length + 1)):
                return length
        return 0

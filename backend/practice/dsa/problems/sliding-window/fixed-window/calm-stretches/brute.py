class Solution:
    def countCalm(self, noise, k, limit):
        return sum(1 for i in range(len(noise) - k + 1) if sum(noise[i:i + k]) / k <= limit)

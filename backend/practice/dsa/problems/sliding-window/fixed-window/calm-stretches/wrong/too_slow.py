class Solution:
    # Mistake: re-adds every window: O(n * k).
    def countCalm(self, noise, k, limit):
        count = 0
        for i in range(len(noise) - k + 1):
            t = 0
            for v in noise[i:i + k]:
                t += v
            if t <= limit * k:
                count += 1
        return count

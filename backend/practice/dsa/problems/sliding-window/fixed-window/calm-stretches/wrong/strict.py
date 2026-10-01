class Solution:
    # Mistake: counts only averages strictly below the limit.
    def countCalm(self, noise, k, limit):
        cap = limit * k
        total = sum(noise[:k])
        count = 1 if total < cap else 0
        for i in range(k, len(noise)):
            total += noise[i] - noise[i - k]
            if total < cap:
                count += 1
        return count

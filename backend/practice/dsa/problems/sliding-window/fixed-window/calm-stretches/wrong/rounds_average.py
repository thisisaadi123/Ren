class Solution:
    # Mistake: rounds the average down first, so a total just over the cap still counts.
    def countCalm(self, noise, k, limit):
        total = sum(noise[:k])
        count = 1 if total // k <= limit else 0
        for i in range(k, len(noise)):
            total += noise[i] - noise[i - k]
            if total // k <= limit:
                count += 1
        return count

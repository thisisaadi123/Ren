class Solution:
    # Mistake: uses the taller post as the level.
    def biggestTank(self, posts):
        i, j = 0, len(posts) - 1
        best = 0
        while i < j:
            best = max(best, (j - i) * max(posts[i], posts[j]))
            if posts[i] < posts[j]:
                i += 1
            else:
                j -= 1
        return best

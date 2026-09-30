class Solution:
    # Mistake: a single bubble pass isn't a full sort.
    def sortScores(self, scores):
        a = scores[:]
        for j in range(len(a) - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
        return a

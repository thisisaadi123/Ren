class Solution:
    def countBreedStretches(self, pens, k):
        n = len(pens)
        return sum(1 for i in range(n) for j in range(i, n) if len(set(pens[i:j + 1])) == k)

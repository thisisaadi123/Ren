class Solution:
    # Mistake: counts stretches with AT MOST k breeds.
    def countBreedStretches(self, pens, k):
        count = {}
        left = total = 0
        for i, v in enumerate(pens):
            count[v] = count.get(v, 0) + 1
            while len(count) > k:
                w = pens[left]
                count[w] -= 1
                if count[w] == 0:
                    del count[w]
                left += 1
            total += i - left + 1
        return total

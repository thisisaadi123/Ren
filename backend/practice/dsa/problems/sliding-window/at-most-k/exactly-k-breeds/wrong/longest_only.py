class Solution:
    # Mistake: for each right edge counts only the longest window with exactly k breeds.
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
            if len(count) == k:
                total += 1
        return total

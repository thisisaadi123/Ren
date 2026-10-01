class Solution:
    # Mistake: stops one window early.
    def varietyPerWindow(self, items, k):
        out = []
        count = {}
        for i in range(len(items) - 1):
            v = items[i]
            count[v] = count.get(v, 0) + 1
            if i >= k:
                w = items[i - k]
                count[w] -= 1
                if count[w] == 0:
                    del count[w]
            if i >= k - 1:
                out.append(len(count))
        return out

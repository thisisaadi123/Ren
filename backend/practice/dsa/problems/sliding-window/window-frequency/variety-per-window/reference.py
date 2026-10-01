class Solution:
    def varietyPerWindow(self, items, k):
        count = {}
        out = []
        for i, v in enumerate(items):
            count[v] = count.get(v, 0) + 1
            if i >= k:
                w = items[i - k]
                count[w] -= 1
                if count[w] == 0:
                    del count[w]
            if i >= k - 1:
                out.append(len(count))
        return out

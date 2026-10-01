class Solution:
    # Mistake: never deletes a type whose count drops to zero, so it still gets counted.
    def varietyPerWindow(self, items, k):
        count = {}
        out = []
        for i, v in enumerate(items):
            count[v] = count.get(v, 0) + 1
            if i >= k:
                count[items[i - k]] -= 1
            if i >= k - 1:
                out.append(len(count))
        return out

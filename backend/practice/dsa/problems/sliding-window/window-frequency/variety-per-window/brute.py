class Solution:
    def varietyPerWindow(self, items, k):
        return [len(set(items[i:i + k])) for i in range(len(items) - k + 1)]

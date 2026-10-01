class Solution:
    # Mistake: rebuilds a set for every window: O(n * k).
    def varietyPerWindow(self, items, k):
        return [len(set(items[i:i + k])) for i in range(len(items) - k + 1)]

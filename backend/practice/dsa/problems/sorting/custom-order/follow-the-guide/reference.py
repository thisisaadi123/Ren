class Solution:
    def orderByGuide(self, items, guide):
        rank = {v: i for i, v in enumerate(guide)}
        big = len(guide)
        return sorted(items, key=lambda x: (rank.get(x, big), x))

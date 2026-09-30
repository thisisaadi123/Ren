class Solution:
    # Mistake: puts unknown items first.
    def orderByGuide(self, items, guide):
        rank = {v: i for i, v in enumerate(guide)}
        return sorted(items, key=lambda x: (rank.get(x, -1), x))

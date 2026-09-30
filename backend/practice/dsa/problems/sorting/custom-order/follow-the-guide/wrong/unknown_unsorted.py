class Solution:
    # Mistake: leaves unknown items in their original order.
    def orderByGuide(self, items, guide):
        rank = {v: i for i, v in enumerate(guide)}
        known = sorted((x for x in items if x in rank), key=rank.get)
        return known + [x for x in items if x not in rank]

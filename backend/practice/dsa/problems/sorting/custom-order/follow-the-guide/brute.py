class Solution:
    def orderByGuide(self, items, guide):
        out = []
        for g in guide:
            out += [x for x in items if x == g]
        out += sorted(x for x in items if x not in guide)
        return out

class Solution:
    def sharedSlots(self, a, b):
        out = []
        for s1, e1 in a:
            for s2, e2 in b:
                s, e = max(s1, s2), min(e1, e2)
                if s <= e:
                    out.append([s, e])
        return sorted(out)

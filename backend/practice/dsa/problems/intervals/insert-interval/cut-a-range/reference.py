class Solution:
    def cutRange(self, slots, cut):
        a, b = cut
        out = []
        for s, e in slots:
            if e <= a or s >= b:
                out.append([s, e])
                continue
            if s < a:
                out.append([s, a])
            if b < e:
                out.append([b, e])
        return out

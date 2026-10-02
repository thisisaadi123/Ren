class Solution:
    # Mistake: assumes the cut lands inside a single slot and stops after trimming the first one it hits.
    def cutRange(self, slots, cut):
        a, b = cut
        out, done = [], False
        for s, e in slots:
            if done or e <= a or s >= b:
                out.append([s, e])
                continue
            if s < a:
                out.append([s, a])
            if b < e:
                out.append([b, e])
            done = True
        return out

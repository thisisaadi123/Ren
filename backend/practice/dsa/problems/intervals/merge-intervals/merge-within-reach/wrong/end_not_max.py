class Solution:
    # Mistake: a shift inside the block shrinks the block's end.
    def mergeWithin(self, shifts, gap):
        out = []
        for s, e in sorted(shifts):
            if out and s - out[-1][1] <= gap:
                out[-1][1] = e
            else:
                out.append([s, e])
        return out

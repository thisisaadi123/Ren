class Solution:
    # Mistake: only joins shifts that overlap or touch.
    def mergeWithin(self, shifts, gap):
        out = []
        for s, e in sorted(shifts):
            if out and s <= out[-1][1]:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([s, e])
        return out

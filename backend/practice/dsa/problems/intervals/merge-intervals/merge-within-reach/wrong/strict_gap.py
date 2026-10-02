class Solution:
    # Mistake: a break of exactly gap minutes starts a new block.
    def mergeWithin(self, shifts, gap):
        out = []
        for s, e in sorted(shifts):
            if out and s - out[-1][1] < gap:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([s, e])
        return out

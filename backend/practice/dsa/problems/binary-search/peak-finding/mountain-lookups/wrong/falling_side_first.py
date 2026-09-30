class Solution:
    # Mistake: checks the falling side first, so a value on both sides returns the larger index.
    def findAltitudes(self, elevations, targets):
        e = elevations
        top = e.index(max(e))
        up, down = e[: top + 1], [-x for x in e[top:]]
        out = []
        for t in targets:
            j = bisect.bisect_left(down, -t)
            if j < len(down) and down[j] == -t:
                out.append(top + j); continue
            i = bisect.bisect_left(up, t)
            out.append(i if i < len(up) and up[i] == t else -1)
        return out

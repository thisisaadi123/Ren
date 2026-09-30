class Solution:
    def findAltitudes(self, elevations, targets):
        e = elevations
        lo, hi = 0, len(e) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if e[mid] < e[mid + 1]:
                lo = mid + 1
            else:
                hi = mid
        top = lo
        up = e[: top + 1]
        down = [-x for x in e[top:]]  # negate so the falling side is ascending too
        out = []
        for t in targets:
            i = bisect.bisect_left(up, t)
            if i < len(up) and up[i] == t:
                out.append(i)
                continue
            j = bisect.bisect_left(down, -t)
            out.append(top + j if j < len(down) and down[j] == -t else -1)
        return out

class Solution:
    def countShorterBehind(self, heights):
        n = len(heights)
        out = [0] * n
        idx = list(range(n))
        buf = [0] * n
        width = 1
        while width < n:
            for lo in range(0, n, 2 * width):
                mid, hi = min(lo + width, n), min(lo + 2 * width, n)
                i, j, k = lo, mid, lo
                while i < mid and j < hi:
                    if heights[idx[j]] < heights[idx[i]]:
                        buf[k] = idx[j]; j += 1
                    else:
                        out[idx[i]] += j - mid
                        buf[k] = idx[i]; i += 1
                    k += 1
                while i < mid:
                    out[idx[i]] += j - mid
                    buf[k] = idx[i]; i += 1; k += 1
                while j < hi:
                    buf[k] = idx[j]; j += 1; k += 1
            idx, buf = buf, idx
            width *= 2
        return out

class Solution:
    def sortScores(self, scores):
        a = scores[:]
        buf = [0] * len(a)
        width = 1
        n = len(a)
        while width < n:
            for lo in range(0, n, 2 * width):
                mid, hi = min(lo + width, n), min(lo + 2 * width, n)
                i, j, k = lo, mid, lo
                while i < mid and j < hi:
                    if a[i] <= a[j]:
                        buf[k] = a[i]; i += 1
                    else:
                        buf[k] = a[j]; j += 1
                    k += 1
                buf[k:k + mid - i] = a[i:mid]; k += mid - i
                buf[k:k + hi - j] = a[j:hi]
            a, buf = buf, a
            width *= 2
        return a

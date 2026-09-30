class Solution:
    # Mistake: treats equal heights as needing a swap.
    def minAdjacentSwaps(self, heights):
        a = heights[:]
        n = len(a)
        buf = [0] * n
        total = 0
        width = 1
        while width < n:
            for lo in range(0, n, 2 * width):
                mid, hi = min(lo + width, n), min(lo + 2 * width, n)
                i, j, k = lo, mid, lo
                while i < mid and j < hi:
                    if a[i] < a[j]:
                        buf[k] = a[i]; i += 1
                    else:
                        buf[k] = a[j]; j += 1
                        total += mid - i
                    k += 1
                buf[k:k + mid - i] = a[i:mid]; k += mid - i
                buf[k:k + hi - j] = a[j:hi]
            a, buf = buf, a
            width *= 2
        return total

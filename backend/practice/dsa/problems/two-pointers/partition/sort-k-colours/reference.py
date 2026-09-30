class Solution:
    def sortKColours(self, balls, k):
        a = balls[:]
        stack = [(0, len(a) - 1, 1, k)]
        while stack:
            left, right, lo, hi = stack.pop()
            if left >= right or lo >= hi:
                continue
            mid = (lo + hi) // 2
            i, j = left, right
            while i <= j:
                while i <= j and a[i] <= mid:
                    i += 1
                while i <= j and a[j] > mid:
                    j -= 1
                if i < j:
                    a[i], a[j] = a[j], a[i]
            stack.append((left, j, lo, mid))
            stack.append((i, right, mid + 1, hi))
        return a

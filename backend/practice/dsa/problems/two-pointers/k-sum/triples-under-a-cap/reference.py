class Solution:
    def countTriplesBelow(self, values, cap):
        a = sorted(values)
        n = len(a)
        total = 0
        for i in range(n - 2):
            j, k = i + 1, n - 1
            while j < k:
                if a[i] + a[j] + a[k] < cap:
                    total += k - j
                    j += 1
                else:
                    k -= 1
        return total

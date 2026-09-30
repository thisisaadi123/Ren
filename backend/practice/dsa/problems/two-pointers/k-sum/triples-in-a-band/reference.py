class Solution:
    def countTriplesInBand(self, values, low, high):
        a = sorted(values)
        n = len(a)
        def at_most(x):
            total = 0
            for i in range(n - 2):
                j, k = i + 1, n - 1
                ai = a[i]
                while j < k:
                    if ai + a[j] + a[k] <= x:
                        total += k - j
                        j += 1
                    else:
                        k -= 1
            return total
        return at_most(high) - at_most(low - 1)

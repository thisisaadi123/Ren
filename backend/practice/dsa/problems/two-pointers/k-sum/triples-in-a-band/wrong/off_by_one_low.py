class Solution:
    # Mistake: subtracts countAtMost(low), dropping sums equal to low.
    def countTriplesInBand(self, values, low, high):
        a = sorted(values)
        n = len(a)
        def at_most(x):
            total = 0
            for i in range(n - 2):
                j, k = i + 1, n - 1
                while j < k:
                    if a[i] + a[j] + a[k] <= x:
                        total += k - j
                        j += 1
                    else:
                        k -= 1
            return total
        return at_most(high) - at_most(low)

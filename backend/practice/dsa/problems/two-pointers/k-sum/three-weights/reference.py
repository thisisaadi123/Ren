class Solution:
    def hasTriple(self, weights, target):
        a = sorted(weights)
        n = len(a)
        for i in range(n - 2):
            j, k = i + 1, n - 1
            while j < k:
                s = a[i] + a[j] + a[k]
                if s == target:
                    return True
                if s < target:
                    j += 1
                else:
                    k -= 1
        return False

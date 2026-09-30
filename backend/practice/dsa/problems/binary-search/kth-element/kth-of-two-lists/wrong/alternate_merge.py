class Solution:
    # Mistake: interleaves the lists instead of merging by value.
    def kthOfTwo(self, a, b, k):
        out = []
        for i in range(max(len(a), len(b))):
            if i < len(a):
                out.append(a[i])
            if i < len(b):
                out.append(b[i])
        return out[k - 1]

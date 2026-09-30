class Solution:
    def kthOfTwo(self, a, b, k):
        return sorted(a + b)[k - 1]

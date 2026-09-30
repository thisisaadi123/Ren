class Solution:
    def kthFree(self, taken, k):
        used = set(taken)
        x = 0
        while k:
            x += 1
            if x not in used:
                k -= 1
        return x

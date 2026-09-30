class Solution:
    def rotateRight(self, slots, k):
        a = slots[:]
        for _ in range(k % len(a)):
            a = [a[-1]] + a[:-1]
        return a

class Solution:
    def rotateRight(self, slots, k):
        a = slots[:]
        for _ in range(k % len(a)):
            a.insert(0, a.pop())
        return a

class Solution:
    def minReadingSpeed(self, books, hours):
        s = 1
        while sum((p + s - 1) // s for p in books) > hours:
            s += 1
        return s

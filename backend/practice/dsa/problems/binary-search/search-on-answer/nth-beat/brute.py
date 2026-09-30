class Solution:
    def nthBeat(self, n, a, b):
        x = 0
        while n:
            x += 1
            if x % a == 0 or x % b == 0:
                n -= 1
        return x % (10**9 + 7)

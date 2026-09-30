class Solution:
    def countMirrors(self, s):
        n = len(s)
        total = 0
        for i in range(n):
            for j in range(i, n):
                a, b = i, j
                while a < b and s[a] == s[b]:
                    a += 1
                    b -= 1
                if a >= b:
                    total += 1
        return total

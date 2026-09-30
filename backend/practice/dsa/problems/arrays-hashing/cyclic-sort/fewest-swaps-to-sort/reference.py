class Solution:
    def minSwaps(self, order):
        n = len(order)
        seen = [False] * n
        cycles = 0
        for i in range(n):
            if not seen[i]:
                cycles += 1
                j = i
                while not seen[j]:
                    seen[j] = True
                    j = order[j] - 1
        return n - cycles

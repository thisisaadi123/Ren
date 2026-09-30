class Solution:
    def kthArrangement(self, n, k):
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i
        left = list(range(1, n + 1))
        k -= 1
        out = []
        for slot in range(n, 0, -1):
            block = fact[slot - 1]
            idx, k = divmod(k, block)
            out.append(left.pop(idx))
        return out

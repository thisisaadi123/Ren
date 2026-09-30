class Solution:
    # Mistake: uses slot! instead of (slot - 1)! as the size of each block.
    def kthArrangement(self, n, k):
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i
        left = list(range(1, n + 1))
        k -= 1
        out = []
        for slot in range(n, 0, -1):
            idx, k = divmod(k, fact[slot])
            out.append(left.pop(idx))
        return out

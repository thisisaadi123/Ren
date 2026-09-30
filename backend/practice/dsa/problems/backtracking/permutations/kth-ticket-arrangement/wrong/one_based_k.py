class Solution:
    # Mistake: forgets to turn k into a 0-based index, so it lands one order too far (and breaks at k = n!).
    def kthArrangement(self, n, k):
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i
        left = list(range(1, n + 1))
        out = []
        for slot in range(n, 0, -1):
            idx, k = divmod(k, fact[slot - 1])
            out.append(left.pop(min(idx, len(left) - 1)))
        return out

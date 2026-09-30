class Solution:
    def tileSums(self, m, k, target):
        out = []
        for mask in range(1 << m):
            pick = [i + 1 for i in range(m) if mask >> i & 1]
            if len(pick) == k and sum(pick) == target:
                out.append(pick)
        return out

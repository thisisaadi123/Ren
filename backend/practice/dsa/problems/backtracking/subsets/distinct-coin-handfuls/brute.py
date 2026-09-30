class Solution:
    def coinHandfuls(self, coins):
        n = len(coins)
        seen = set()
        for mask in range(1 << n):
            seen.add(tuple(sorted(coins[i] for i in range(n) if mask >> i & 1)))
        return [list(t) for t in seen]

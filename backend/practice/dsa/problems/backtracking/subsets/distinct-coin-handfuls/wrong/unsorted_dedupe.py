class Solution:
    # Mistake: dedupes with a set of tuples but never sorts, so [1, 2] and [2, 1] both survive.
    def coinHandfuls(self, coins):
        n = len(coins)
        seen = set()
        for mask in range(1 << n):
            seen.add(tuple(coins[i] for i in range(n) if mask >> i & 1))
        return [list(t) for t in seen]

class Solution:
    # Mistake: scans forward from every start: O(n^2) when one letter is rare.
    def countFullSets(self, s):
        n = len(s)
        total = 0
        for i in range(n):
            seen = set()
            for j in range(i, n):
                seen.add(s[j])
                if len(seen) == 3:
                    total += n - j
                    break
        return total

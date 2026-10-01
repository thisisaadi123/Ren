class Solution:
    # Mistake: tries every start: O(n^2).
    def shortestNetGain(self, changes, target):
        n = len(changes)
        best = n + 1
        for i in range(n):
            s = 0
            for j in range(i, min(n, i + best)):
                s += changes[j]
                if s >= target:
                    best = j - i + 1
                    break
        return best if best <= n else -1

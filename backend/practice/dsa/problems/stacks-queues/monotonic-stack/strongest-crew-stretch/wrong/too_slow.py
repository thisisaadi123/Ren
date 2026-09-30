class Solution:
    # Mistake: tries every start and grows the crew one worker at a time: O(n²).
    def strongestCrew(self, strength):
        n = len(strength)
        best = 0
        for i in range(n):
            lo, total = strength[i], 0
            for j in range(i, n):
                lo = min(lo, strength[j])
                total += strength[j]
                best = max(best, lo * total)
        return best

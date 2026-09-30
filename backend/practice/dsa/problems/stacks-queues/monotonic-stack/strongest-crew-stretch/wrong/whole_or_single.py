class Solution:
    # Mistake: assumes the best crew is either everyone or a single strongest worker.
    def strongestCrew(self, strength):
        return max(min(strength) * sum(strength), max(strength) ** 2)

class Solution:
    # Mistake: only checks that the total divides evenly.
    def equalTeams(self, scores, k):
        return sum(scores) % k == 0 and max(scores) <= sum(scores) // k

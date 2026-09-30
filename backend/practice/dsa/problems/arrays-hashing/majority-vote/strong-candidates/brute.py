class Solution:
    def strongCandidates(self, votes):
        n = len(votes)
        return sorted(v for v in set(votes) if votes.count(v) > n // 3)

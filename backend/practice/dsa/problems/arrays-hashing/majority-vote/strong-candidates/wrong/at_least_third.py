class Solution:
    # Mistake: uses >= instead of >.
    def strongCandidates(self, votes):
        n = len(votes)
        return sorted(v for v in set(votes) if 3 * votes.count(v) >= n)

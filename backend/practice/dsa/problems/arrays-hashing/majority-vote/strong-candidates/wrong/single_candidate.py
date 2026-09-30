class Solution:
    # Mistake: tracks only one candidate.
    def strongCandidates(self, votes):
        cand, count = None, 0
        for v in votes:
            if count == 0:
                cand = v
            count += 1 if v == cand else -1
        return [cand] if votes.count(cand) > len(votes) // 3 else []

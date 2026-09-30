class Solution:
    def strictMajority(self, votes):
        cand, count = None, 0
        for v in votes:
            if count == 0:
                cand = v
            count += 1 if v == cand else -1
        return cand if votes.count(cand) * 2 > len(votes) else -1

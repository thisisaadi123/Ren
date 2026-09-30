class Solution:
    def strongCandidates(self, votes):
        n = len(votes)
        out = []
        for i, v in enumerate(votes):
            if v not in out and sum(1 for w in votes if w == v) > n // 3:
                out.append(v)
        return sorted(out)

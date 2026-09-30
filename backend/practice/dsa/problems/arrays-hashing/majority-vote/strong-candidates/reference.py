class Solution:
    def strongCandidates(self, votes):
        a = b = None
        ca = cb = 0
        for v in votes:
            if v == a:
                ca += 1
            elif v == b:
                cb += 1
            elif ca == 0:
                a, ca = v, 1
            elif cb == 0:
                b, cb = v, 1
            else:
                ca -= 1
                cb -= 1
        n = len(votes)
        return sorted(c for c in {a, b} if c is not None and votes.count(c) > n // 3)

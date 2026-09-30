class Solution:
    # Mistake: trusts the Boyer-Moore candidate without checking it.
    def strictMajority(self, votes):
        cand, count = None, 0
        for v in votes:
            if count == 0:
                cand = v
            count += 1 if v == cand else -1
        return cand

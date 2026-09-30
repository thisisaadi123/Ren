class Solution:
    def strictMajority(self, votes):
        for v in set(votes):
            if votes.count(v) * 2 > len(votes):
                return v
        return -1

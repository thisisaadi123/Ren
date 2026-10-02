class Solution:
    # Mistake: puts each player in the first team with room and never backtracks.
    def equalTeams(self, scores, k):
        total = sum(scores)
        if total % k:
            return False
        target = total // k
        load = [0] * k
        for x in scores:
            for t in range(k):
                if load[t] + x <= target:
                    load[t] += x
                    break
            else:
                return False
        return True

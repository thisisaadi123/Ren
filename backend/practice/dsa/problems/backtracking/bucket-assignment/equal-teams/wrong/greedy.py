class Solution:
    # Mistake: drops each player into the lightest team that fits, never undoing a choice.
    def equalTeams(self, scores, k):
        total = sum(scores)
        if total % k:
            return False
        target = total // k
        load = [0] * k
        for x in sorted(scores, reverse=True):
            t = min(range(k), key=lambda t: load[t])
            if load[t] + x > target:
                return False
            load[t] += x
        return True

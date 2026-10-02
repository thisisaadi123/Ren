class Solution:
    def equalTeams(self, scores, k):
        total = sum(scores)
        if total % k:
            return False
        target = total // k
        xs = sorted(scores, reverse=True)
        if xs[0] > target:
            return False
        load = [0] * k

        def go(i):
            if i == len(xs):
                return True
            tried = set()
            for t in range(k):
                if load[t] + xs[i] <= target and load[t] not in tried:
                    tried.add(load[t])
                    load[t] += xs[i]
                    if go(i + 1):
                        return True
                    load[t] -= xs[i]
            return False

        return go(0)

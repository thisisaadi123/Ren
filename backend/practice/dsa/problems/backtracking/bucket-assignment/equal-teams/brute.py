class Solution:
    def equalTeams(self, scores, k):
        total = sum(scores)
        if total % k:
            return False
        target = total // k
        n = len(scores)
        best = {0: 0}
        for mask in range(1 << n):
            if mask not in best:
                continue
            cur = best[mask]
            for i in range(n):
                if not mask >> i & 1 and cur + scores[i] <= target:
                    best.setdefault(mask | 1 << i, (cur + scores[i]) % target)
        return (1 << n) - 1 in best

class Solution:
    def secondsToFinish(self, wants, k):
        need = wants[k]
        return sum(min(w, need) if i <= k else min(w, need - 1) for i, w in enumerate(wants))

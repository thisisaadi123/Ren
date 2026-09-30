class Solution:
    def insertPosition(self, scores, target):
        for i, s in enumerate(scores):
            if s >= target:
                return i
        return len(scores)

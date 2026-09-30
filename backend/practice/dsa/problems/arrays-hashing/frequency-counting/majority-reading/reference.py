class Solution:
    def majorityValue(self, readings):
        candidate, count = None, 0
        for r in readings:
            if count == 0:
                candidate = r
            count += 1 if r == candidate else -1
        return candidate

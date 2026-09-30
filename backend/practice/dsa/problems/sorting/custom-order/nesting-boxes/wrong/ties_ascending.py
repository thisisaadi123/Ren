import bisect
class Solution:
    # Mistake: sorts equal widths by height ascending, so they chain.
    def maxNested(self, boxes):
        tails = []
        for w, h in sorted(boxes):
            i = bisect.bisect_left(tails, h)
            if i == len(tails):
                tails.append(h)
            else:
                tails[i] = h
        return len(tails)

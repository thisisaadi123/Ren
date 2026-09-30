import bisect
class Solution:
    # Mistake: allows equal heights to nest.
    def maxNested(self, boxes):
        tails = []
        for w, h in sorted(boxes, key=lambda b: (b[0], -b[1])):
            i = bisect.bisect_right(tails, h)
            if i == len(tails):
                tails.append(h)
            else:
                tails[i] = h
        return len(tails)

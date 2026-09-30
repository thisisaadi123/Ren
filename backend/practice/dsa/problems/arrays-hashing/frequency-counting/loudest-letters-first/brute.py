class Solution:
    def sortByFrequency(self, s):
        out, left = [], sorted(set(s))
        while left:
            best = left[0]
            for c in left:
                if s.count(c) > s.count(best):
                    best = c
            out.append(best * s.count(best))
            left.remove(best)
        return "".join(out)

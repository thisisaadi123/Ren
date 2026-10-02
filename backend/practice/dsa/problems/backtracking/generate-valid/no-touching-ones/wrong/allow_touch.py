class Solution:
    # Mistake: forgets the no-touching rule.
    def spacedStrings(self, n, ones):
        out = []
        for m in range(1 << n):
            s = format(m, "0%db" % n)
            if s.count("1") == ones:
                out.append(s)
        return out

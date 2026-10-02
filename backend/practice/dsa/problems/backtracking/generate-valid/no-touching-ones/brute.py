class Solution:
    def spacedStrings(self, n, ones):
        out = []
        for m in range(1 << n):
            s = format(m, "0%db" % n)
            if s.count("1") == ones and "11" not in s:
                out.append(s)
        return out

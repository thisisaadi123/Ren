import itertools
class Solution:
    def compress(self, text):
        out = ""
        for c, grp in itertools.groupby(text):
            k = len(list(grp))
            out += c + (str(k) if k > 1 else "")
        return out

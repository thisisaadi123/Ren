class Solution:
    # Mistake: jumps past a match, so overlapping copies are missed.
    def findAll(self, text, tag):
        out, i = [], text.find(tag)
        while i != -1:
            out.append(i)
            i = text.find(tag, i + len(tag))
        return out

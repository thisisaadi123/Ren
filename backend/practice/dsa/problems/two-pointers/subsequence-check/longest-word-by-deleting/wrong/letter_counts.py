import collections
class Solution:
    # Mistake: checks letter counts but not their order.
    def longestByDeleting(self, text, dictionary):
        have = collections.Counter(text)
        ok = [w for w in dictionary if not collections.Counter(w) - have]
        return min(ok, key=lambda w: (-len(w), w)) if ok else ""

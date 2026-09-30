class Solution:
    def longestByDeleting(self, text, dictionary):
        def hidden(w):
            it = iter(text)
            return all(c in it for c in w)
        ok = [w for w in dictionary if hidden(w)]
        return min(ok, key=lambda w: (-len(w), w)) if ok else ""

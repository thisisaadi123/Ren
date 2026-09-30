class Solution:
    # Mistake: on ties keeps the first word found, not the alphabetically first.
    def longestByDeleting(self, text, dictionary):
        def hidden(w):
            it = iter(text)
            return all(c in it for c in w)
        best = ""
        for w in dictionary:
            if len(w) > len(best) and hidden(w):
                best = w
        return best

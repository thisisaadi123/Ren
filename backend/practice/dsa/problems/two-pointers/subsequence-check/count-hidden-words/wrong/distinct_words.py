class Solution:
    # Mistake: counts each distinct word once.
    def countHidden(self, text, words):
        def hidden(w):
            it = iter(text)
            return all(c in it for c in w)
        return sum(1 for w in set(words) if hidden(w))

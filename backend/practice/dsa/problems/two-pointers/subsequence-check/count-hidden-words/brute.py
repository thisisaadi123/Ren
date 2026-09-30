class Solution:
    def countHidden(self, text, words):
        def hidden(w):
            it = iter(text)
            return all(c in it for c in w)
        return sum(1 for w in words if hidden(w))

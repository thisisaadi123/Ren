class Solution:
    def longestByDeleting(self, text, dictionary):
        def hidden(w):
            i = 0
            for c in text:
                if i < len(w) and c == w[i]:
                    i += 1
            return i == len(w)
        best = ""
        for w in dictionary:
            if (len(w) > len(best) or (len(w) == len(best) and w < best)) and hidden(w):
                best = w
        return best

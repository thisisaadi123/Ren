class Solution:
    def countHidden(self, text, words):
        total = 0
        for w in words:
            i = 0
            for c in text:
                if i < len(w) and c == w[i]:
                    i += 1
            total += i == len(w)
        return total

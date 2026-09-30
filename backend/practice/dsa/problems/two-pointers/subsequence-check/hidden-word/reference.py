class Solution:
    def isHidden(self, word, text):
        i = 0
        for c in text:
            if i < len(word) and c == word[i]:
                i += 1
        return i == len(word)

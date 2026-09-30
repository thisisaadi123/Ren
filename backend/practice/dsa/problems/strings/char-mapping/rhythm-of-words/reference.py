class Solution:
    def followsRhythm(self, pattern, sentence):
        words = sentence.split(" ")
        if len(words) != len(pattern):
            return False
        to_word, to_letter = {}, {}
        for p, w in zip(pattern, words):
            if to_word.setdefault(p, w) != w or to_letter.setdefault(w, p) != p:
                return False
        return True

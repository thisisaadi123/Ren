class Solution:
    # Mistake: zips the two sequences without checking they have the same length.
    def followsRhythm(self, pattern, sentence):
        to_word, to_letter = {}, {}
        for p, w in zip(pattern, sentence.split(" ")):
            if to_word.setdefault(p, w) != w or to_letter.setdefault(w, p) != p:
                return False
        return True

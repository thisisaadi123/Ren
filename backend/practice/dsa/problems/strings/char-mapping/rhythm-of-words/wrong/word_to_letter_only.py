class Solution:
    # Mistake: only checks word → letter, so one letter may stand for two words.
    def followsRhythm(self, pattern, sentence):
        words = sentence.split(" ")
        if len(words) != len(pattern):
            return False
        to_letter = {}
        for p, w in zip(pattern, words):
            if to_letter.setdefault(w, p) != p:
                return False
        return True

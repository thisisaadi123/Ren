class Solution:
    # Mistake: only checks letter → word, so two letters may share one word.
    def followsRhythm(self, pattern, sentence):
        words = sentence.split(" ")
        if len(words) != len(pattern):
            return False
        to_word = {}
        for p, w in zip(pattern, words):
            if to_word.setdefault(p, w) != w:
                return False
        return True

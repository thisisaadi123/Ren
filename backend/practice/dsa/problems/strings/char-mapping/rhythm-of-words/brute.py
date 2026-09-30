class Solution:
    def followsRhythm(self, pattern, sentence):
        words = sentence.split()
        if len(words) != len(pattern):
            return False
        n = len(words)
        return all((pattern[i] == pattern[j]) == (words[i] == words[j]) for i in range(n) for j in range(n))

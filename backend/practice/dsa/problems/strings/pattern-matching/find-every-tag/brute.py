class Solution:
    def findAll(self, text, tag):
        return [i for i in range(len(text) - len(tag) + 1) if text[i:i + len(tag)] == tag]

class Solution:
    def reverseLetters(self, text):
        letters = [c for c in text if c.isalpha()]
        return "".join(letters.pop() if c.isalpha() else c for c in text)

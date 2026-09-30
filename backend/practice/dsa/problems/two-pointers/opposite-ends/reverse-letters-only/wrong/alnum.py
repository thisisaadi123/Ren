class Solution:
    # Mistake: treats digits as letters too.
    def reverseLetters(self, text):
        chars = [c for c in text if c.isalnum()]
        return "".join(chars.pop() if c.isalnum() else c for c in text)

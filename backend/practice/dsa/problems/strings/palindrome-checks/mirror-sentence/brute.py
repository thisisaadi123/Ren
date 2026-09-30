class Solution:
    def isMirror(self, text):
        kept = [c.lower() for c in text if c.isalnum()]
        return kept == kept[::-1]

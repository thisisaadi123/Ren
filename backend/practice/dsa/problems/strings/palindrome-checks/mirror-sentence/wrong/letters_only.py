class Solution:
    # Mistake: throws away digits as well, but digits must match too.
    def isMirror(self, text):
        kept = [c.lower() for c in text if c.isalpha()]
        return kept == kept[::-1]

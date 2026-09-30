class Solution:
    # Mistake: compares letters without ignoring case.
    def isMirror(self, text):
        kept = [c for c in text if c.isalnum()]
        return kept == kept[::-1]

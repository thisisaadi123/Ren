class Solution:
    # Mistake: removes spaces but keeps punctuation in the comparison.
    def isMirror(self, text):
        kept = [c.lower() for c in text if c != " "]
        return kept == kept[::-1]

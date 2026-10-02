class Solution:
    # Mistake: lets a pattern match the start of a longer word.
    def countMatches(self, words, patterns):
        return [sum(1 for w in words if len(w) >= len(p) and all(a == "." or a == b for a, b in zip(p, w))) for p in patterns]

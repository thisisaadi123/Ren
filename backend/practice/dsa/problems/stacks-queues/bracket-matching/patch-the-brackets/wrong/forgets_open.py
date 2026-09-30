class Solution:
    # Mistake: patches unmatched `)` but forgets the `(` still open at the end.
    def minInsertions(self, s):
        open_, added = 0, 0
        for c in s:
            if c == "(":
                open_ += 1
            elif open_:
                open_ -= 1
            else:
                added += 1
        return added

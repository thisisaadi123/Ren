class Solution:
    # Mistake: only produces fully nested and fully flat strings.
    def buildBrackets(self, n):
        return sorted({"(" * n + ")" * n, "()" * n})

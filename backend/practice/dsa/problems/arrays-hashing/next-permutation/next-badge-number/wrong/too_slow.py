class Solution:
    # Mistake: rescans the whole tail for every position: O(n^2).
    def nextBadge(self, code):
        for i in range(len(code) - 2, -1, -1):
            bigger = [c for c in code[i + 1:] if c > code[i]]
            if bigger:
                d = min(bigger)
                rest = list(code[i:])
                rest.remove(d)
                return code[:i] + d + "".join(sorted(rest))
        return ""

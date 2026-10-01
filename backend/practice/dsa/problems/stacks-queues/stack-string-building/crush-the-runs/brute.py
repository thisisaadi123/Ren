class Solution:
    def crushRuns(self, s, k):
        changed = True
        while changed:
            changed = False
            for i in range(len(s) - k + 1):
                if s[i] * k == s[i:i + k]:
                    s = s[:i] + s[i + k:]
                    changed = True
                    break
        return s

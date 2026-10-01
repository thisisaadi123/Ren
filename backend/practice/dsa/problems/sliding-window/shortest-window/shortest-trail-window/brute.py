class Solution:
    def trailWindow(self, s, t):
        def has(part):
            it = iter(part)
            return all(c in it for c in t)

        for length in range(len(t), len(s) + 1):
            for i in range(len(s) - length + 1):
                if has(s[i:i + length]):
                    return s[i:i + length]
        return ""

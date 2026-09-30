class Solution:
    def isScramble(self, a, b):
        cnt = [0] * 26
        for c in a:
            if c != " ":
                cnt[(ord(c) | 32) - 97] += 1
        for c in b:
            if c != " ":
                cnt[(ord(c) | 32) - 97] -= 1
        return not any(cnt)

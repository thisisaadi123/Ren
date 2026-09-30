class Solution:
    def padToPalindrome(self, s):
        for k in range(len(s), -1, -1):
            p = s[:k]
            if p == p[::-1]:
                return s[k:][::-1] + s
